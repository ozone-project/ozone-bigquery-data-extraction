#!/usr/bin/env python3
"""
Run the BigQuery Data Extraction API server.
"""

import uvicorn
from src.config import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )