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

#### BigQuery Endpoints
- `POST /query`: Execute custom SQL queries with optional parameters
  - Body: `{"query": "SELECT * FROM table", "parameters": {"param": "value"}}`
- `GET /datasets`: List all datasets in the project
- `GET /datasets/{dataset_id}/tables`: List tables in a specific dataset
- `GET /datasets/{dataset_id}/tables/{table_id}/schema`: Get schema for a specific table

#### Domain Analytics Endpoints
- `GET /fill-rate?domain={domain}`: Get fill rate data from 30 days ago for a specific domain
  - Returns ad requests, impressions, and fill rates by ad unit
- `GET /attention?domain={domain}`: Get attention metrics from the last 30 days
  - Returns tracker clicks and viewable impressions for the domain
- `GET /domain-history?domain={domain}&ad_unit_ids={unit1}&ad_unit_ids={unit2}`: Get domain performance history from yesterday
  - Optional `ad_unit_ids` parameter to filter by specific ad units
  - Returns bid rates, CPMs, win rates, fill rates, and revenue data
- `GET /domain-site-info?domain={domain}`: Get publisher information from Sincera database
  - Returns publisher details, performance metrics, and supply chain data from `sincera_data.db`

#### System Endpoints
- `GET /health`: Health check with BigQuery connectivity status
- `GET /`: Root endpoint returning API status

### Example Usage

See `examples/api_usage.py` for programmatic API client and `examples/sample_queries.py` for common BigQuery patterns.

## Authentication

Uses Google Cloud service account authentication. Ensure the service account has BigQuery Data Viewer permissions and the credentials file is properly configured.