from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    row_count: int


class SchemaField(BaseModel):
    name: str
    type: str
    mode: str
    description: Optional[str] = None


class SchemaResponse(BaseModel):
    fields: List[SchemaField]


class DatasetListResponse(BaseModel):
    datasets: List[str]


class TableListResponse(BaseModel):
    tables: List[str]


class FillRateRecord(BaseModel):
    publisher_id: Optional[str] = None
    domain: Optional[str] = None
    ad_unit_id: Optional[str] = None
    ad_requests_est: Optional[float] = None
    impressions_est: Optional[float] = None
    fill_rate: Optional[float] = None


class FillRateResponse(BaseModel):
    data: List[FillRateRecord]
    row_count: int


class AttentionRecord(BaseModel):
    domain: Optional[str] = None
    publisher_id: Optional[str] = None
    tracker_ad_clicks: Optional[float] = None
    tracker_ad_hovers: Optional[float] = None
    vie_imps: Optional[float] = None
    vie_pct: Optional[float] = None
    hover_pct: Optional[float] = None
    click_pct: Optional[float] = None


class AttentionResponse(BaseModel):
    data: List[AttentionRecord]
    row_count: int


class DomainHistoryRecord(BaseModel):
    publisher_id: Optional[str] = None
    domain: Optional[str] = None
    ad_unit_id: Optional[str] = None
    ad_requests_est: Optional[float] = None
    rev_oz_net_usd: Optional[float] = None
    bid_rate: Optional[float] = None
    bid_cpm: Optional[float] = None
    win_rate: Optional[float] = None
    fill_rate: Optional[float] = None
    impression_cpm: Optional[float] = None


class DomainHistoryResponse(BaseModel):
    data: List[DomainHistoryRecord]
    row_count: int


class DomainSiteInfoRecord(BaseModel):
    domain: str
    publisher_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[str] = None
    primary_supply_type: Optional[str] = None
    pub_description: Optional[str] = None
    categories: Optional[List[str]] = None
    slug: Optional[str] = None
    avg_ads_to_content_ratio: Optional[float] = None
    avg_ads_in_view: Optional[float] = None
    avg_ad_refresh: Optional[float] = None
    total_unique_gpids: Optional[int] = None
    id_absorption_rate: Optional[float] = None
    avg_page_weight: Optional[float] = None
    avg_cpu: Optional[float] = None
    total_supply_paths: Optional[int] = None
    reseller_count: Optional[int] = None
    owner_domain: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class DomainSiteInfoResponse(BaseModel):
    data: Optional[DomainSiteInfoRecord] = None
    found: bool
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None