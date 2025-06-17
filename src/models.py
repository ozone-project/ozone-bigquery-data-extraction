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
    tracker_clicks: Optional[float] = None
    vie_imps: Optional[float] = None


class AttentionResponse(BaseModel):
    data: List[AttentionRecord]
    row_count: int


class DomainHistoryRecord(BaseModel):
    publisher_id: Optional[str] = None
    domain: Optional[str] = None
    ad_unit_id: Optional[str] = None
    ad_requests_est: Optional[float] = None
    bid_rate: Optional[float] = None
    bid_cpm: Optional[float] = None
    win_rate: Optional[float] = None
    fill_rate: Optional[float] = None
    impression_cpm: Optional[float] = None


class DomainHistoryResponse(BaseModel):
    data: List[DomainHistoryRecord]
    row_count: int


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None