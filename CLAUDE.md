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

- `POST /query`: Execute SQL queries with optional parameters
- `GET /datasets`: List all datasets in the project
- `GET /datasets/{dataset_id}/tables`: List tables in a dataset
- `GET /datasets/{dataset_id}/tables/{table_id}/schema`: Get table schema
- `GET /fill-rate`: Get fill rate data from yesterday for a specific domain
- `GET /attention`: Get attention metrics from the last 30 days
- `GET /health`: Health check with BigQuery connectivity status

### Example Usage

See `examples/api_usage.py` for programmatic API client and `examples/sample_queries.py` for common BigQuery patterns.

## Authentication

Uses Google Cloud service account authentication. Ensure the service account has BigQuery Data Viewer permissions and the credentials file is properly configured.