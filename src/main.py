from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from .bigquery_client import BigQueryClient
from .models import (
    QueryRequest, QueryResponse, SchemaResponse, 
    DatasetListResponse, TableListResponse, ErrorResponse,
    FillRateResponse, FillRateRecord, AttentionResponse, AttentionRecord,
    DomainHistoryResponse, DomainHistoryRecord
)

load_dotenv()

app = FastAPI(
    title="BigQuery Data Extraction API",
    description="API for extracting data from BigQuery",
    version="1.0.0"
)

try:
    bq_client = BigQueryClient()
except Exception as e:
    print(f"Failed to initialize BigQuery client: {e}")
    bq_client = None


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Internal server error", detail=str(exc)).dict()
    )


@app.get("/")
async def root():
    return {"message": "BigQuery Data Extraction API", "status": "running"}


@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute a BigQuery SQL query"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    try:
        results = bq_client.execute_query(request.query, request.parameters)
        return QueryResponse(data=results, row_count=len(results))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/datasets", response_model=DatasetListResponse)
async def list_datasets():
    """List all datasets in the project"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    try:
        datasets = bq_client.list_datasets()
        return DatasetListResponse(datasets=datasets)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/datasets/{dataset_id}/tables", response_model=TableListResponse)
async def list_tables(dataset_id: str):
    """List all tables in a dataset"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    try:
        tables = bq_client.list_tables(dataset_id)
        return TableListResponse(tables=tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/datasets/{dataset_id}/tables/{table_id}/schema", response_model=SchemaResponse)
async def get_table_schema(dataset_id: str, table_id: str):
    """Get the schema of a specific table"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    try:
        schema = bq_client.get_table_schema(dataset_id, table_id)
        return SchemaResponse(fields=schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/fill-rate", response_model=FillRateResponse)
async def get_fill_rate(domain: str):
    """Get fill rate data from yesterday for a specific domain"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    fill_rate_query = """
    SELECT
        publisher_id,
        domain,
        ad_unit_id_feature as ad_init_id,
        sum(ad_requests_est) as ad_requests_est,
        sum(impressions_est) as impressions_est,
        safe_divide(sum(impressions_est),sum(ad_requests_est)) as fill_rate
    FROM ozone.fct_smart_bidstream__root
    WHERE date(date_hour) = current_date - 30
        AND domain = @domain
    GROUP BY ALL
    HAVING ad_requests_est > 1000000
    ORDER BY ad_requests_est DESC
    """
    
    try:
        results = bq_client.execute_query(fill_rate_query, {"domain": domain})
        fill_rate_records = [FillRateRecord(**record) for record in results]
        return FillRateResponse(data=fill_rate_records, row_count=len(fill_rate_records))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/attention", response_model=AttentionResponse)
async def get_attention_metrics(domain: str):
    """Get attention metrics from the last 30 days for a specific domain"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    attention_query = """
    SELECT 
        dv_delivery_domain as domain, 
        publisher_id, 
        sum(tracker_ad_clicks) as tracker_clicks, 
        sum(dv_net_iab_viewable_imp) as vie_imps
    FROM `ozpr-data-engineering-prod.prod_de_attention_metrics.fct_attention_metrics__beeswax`
    WHERE date(ts) >= current_date - 30
        AND dv_delivery_domain is not null
        AND dv_delivery_domain = @domain
    GROUP BY ALL
    """
    
    try:
        results = bq_client.execute_query(attention_query, {"domain": domain})
        attention_records = [AttentionRecord(**record) for record in results]
        return AttentionResponse(data=attention_records, row_count=len(attention_records))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/domain-history", response_model=DomainHistoryResponse)
async def get_domain_history(domain: str):
    """Get domain history data from yesterday for a specific domain"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="BigQuery client not initialized")
    
    domain_history_query = """
    select
      publisher_id,
      domain,
      ad_unit_id_feature as ad_unit_id,
      sum(ad_requests_est) as ad_requests_est,

      safe_divide(
        sum(ad_bids),
        sum(ad_requests_est)
      ) as bid_rate,

      safe_divide(
        sum(ad_rev_bid_net_usd),
        sum(ad_bids)
      ) *1000 as bid_cpm,

      safe_divide(
        sum(impressions_est),
        sum(ad_bids)
      ) as win_rate,

      safe_divide(
        sum(impressions_est),
        sum(ad_requests_est)
      ) as fill_rate,

      safe_divide(
        sum(ad_rev_oz_net_usd_est),
        sum(impressions_est)
      ) *1000 as impression_cpm,

    from ozone.fct_smart_bidstream__root
    where date(date_hour) = current_date - 1
    and domain = @domain
    group by all
    """
    
    try:
        results = bq_client.execute_query(domain_history_query, {"domain": domain})
        domain_history_records = [DomainHistoryRecord(**record) for record in results]
        return DomainHistoryResponse(data=domain_history_records, row_count=len(domain_history_records))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if not bq_client:
        return {"status": "unhealthy", "error": "BigQuery client not initialized"}
    
    try:
        bq_client.list_datasets()
        return {"status": "healthy", "bigquery": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}