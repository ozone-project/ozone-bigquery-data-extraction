# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python FastAPI server that acts as a BigQuery client for extracting data from BigQuery instances via standard API endpoints.

## Development Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and configure:
   - `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON key
3. Run server: `python run_server.py`

## Commands

- `python run_server.py`: Start the FastAPI server with auto-reload
- `uvicorn src.main:app --reload`: Alternative way to run the server
- Server runs on `http://localhost:8000` by default

## Architecture

### Core Components

- `src/bigquery_client.py`: BigQuery client wrapper with query execution, schema inspection, and dataset/table listing
- `src/main.py`: FastAPI application with REST endpoints
- `src/models.py`: Pydantic models for request/response validation  
- `src/config.py`: Configuration management using environment variables

### API Endpoints

#### System Endpoints

##### `GET /`
Root endpoint returning API status.

**Response:**
```json
{
  "message": "BigQuery Data Extraction API",
  "status": "running" 
}
```

##### `GET /health`
Health check endpoint with BigQuery connectivity status.

**Response (healthy):**
```json
{
  "status": "healthy",
  "bigquery": "connected"
}
```

**Response (unhealthy):**
```json
{
  "status": "unhealthy", 
  "error": "error description"
}
```

#### BigQuery Endpoints

##### `POST /query`
Execute custom SQL queries with optional parameters.

**Request Body:**
```json
{
  "query": "SELECT * FROM table WHERE field = @param",
  "parameters": {
    "param": "value"
  }
}
```

**Response:**
```json
{
  "data": [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ],
  "row_count": 2
}
```

##### `GET /datasets`
List all datasets in the project.

**Response:**
```json
{
  "datasets": ["dataset1", "dataset2", "dataset3"]
}
```

##### `GET /datasets/{dataset_id}/tables`
List all tables in a specific dataset.

**Parameters:**
- `dataset_id` (path): ID of the dataset

**Response:**
```json
{
  "tables": ["table1", "table2", "table3"]
}
```

##### `GET /datasets/{dataset_id}/tables/{table_id}/schema`
Get the schema of a specific table.

**Parameters:**
- `dataset_id` (path): ID of the dataset
- `table_id` (path): ID of the table

**Response:**
```json
{
  "fields": [
    {
      "name": "column_name",
      "type": "STRING",
      "mode": "NULLABLE",
      "description": "Column description"
    }
  ]
}
```

#### Domain Analytics Endpoints

##### `GET /fill-rate?domain={domain}`
Get fill rate data from 30 days ago for a specific domain. Returns data for ad units with >1M ad requests.

**Parameters:**
- `domain` (query): Domain name to analyze

**Response:**
```json
{
  "data": [
    {
      "publisher_id": "12345",
      "domain": "example.com",
      "ad_unit_id": "unit123",
      "ad_requests_est": 5000000.0,
      "impressions_est": 3500000.0,
      "fill_rate": 0.7
    }
  ],
  "row_count": 1
}
```

**Example:**
```bash
curl "http://localhost:8000/fill-rate?domain=example.com"
```

##### `GET /attention?domain={domain}`
Get attention metrics from the last 7 days for a specific domain.

**Parameters:**
- `domain` (query): Domain name to analyze

**Response:**
```json
{
  "data": [
    {
      "domain": "example.com",
      "publisher_id": "12345",
      "tracker_clicks": 1500.0,
      "vie_imps": 2500000.0
    }
  ],
  "row_count": 1
}
```

**Example:**
```bash
curl "http://localhost:8000/attention?domain=example.com"
```

##### `GET /domain-history?domain={domain}&ad_unit_ids={unit1}&ad_unit_ids={unit2}`
Get domain performance history from yesterday for a specific domain, optionally filtered by ad unit IDs.

**Parameters:**
- `domain` (query, required): Domain name to analyze
- `ad_unit_ids` (query, optional): List of ad unit IDs to filter by (can specify multiple)

**Response:**
```json
{
  "data": [
    {
      "publisher_id": "12345",
      "domain": "example.com", 
      "ad_unit_id": "unit123",
      "ad_requests_est": 1000000.0,
      "rev_oz_net_usd": 2500.0,
      "bid_rate": 0.85,
      "bid_cpm": 3.25,
      "win_rate": 0.42,
      "fill_rate": 0.36,
      "impression_cpm": 6.94
    }
  ],
  "row_count": 1
}
```

**Examples:**
```bash
# All ad units for domain
curl "http://localhost:8000/domain-history?domain=example.com"

# Specific ad units only
curl "http://localhost:8000/domain-history?domain=example.com&ad_unit_ids=unit123&ad_unit_ids=unit456"
```

##### `GET /domain-site-info?domain={domain}`
Get publisher information from the Sincera database for a specific domain.

**Parameters:**
- `domain` (query): Domain name to look up

**Response (found):**
```json
{
  "data": {
    "domain": "example.com",
    "publisher_id": 12345,
    "name": "Example Publisher",
    "status": "active",
    "primary_supply_type": "direct",
    "pub_description": "Publisher description",
    "categories": ["news", "sports"],
    "slug": "example-publisher",
    "avg_ads_to_content_ratio": 0.15,
    "avg_ads_in_view": 2.3,
    "avg_ad_refresh": 30.0,
    "total_unique_gpids": 150,
    "id_absorption_rate": 0.85,
    "avg_page_weight": 2.5,
    "avg_cpu": 45.2,
    "total_supply_paths": 8,
    "reseller_count": 12,
    "owner_domain": "parent-company.com",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-06-10T14:25:00Z"
  },
  "found": true,
  "message": "Domain information found for example.com"
}
```

**Response (not found):**
```json
{
  "data": null,
  "found": false,
  "message": "No information found for domain example.com"
}
```

**Example:**
```bash
curl "http://localhost:8000/domain-site-info?domain=example.com"
```

### Example Usage

See `examples/api_usage.py` for programmatic API client and `examples/sample_queries.py` for common BigQuery patterns.

## Authentication

Uses Google Cloud service account authentication. Ensure the service account has BigQuery Data Viewer permissions and the credentials file is properly configured.