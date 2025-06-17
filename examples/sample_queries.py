"""
Sample queries for BigQuery data extraction.
These examples show common patterns for extracting data from BigQuery tables.
"""

SAMPLE_QUERIES = {
    "get_table_info": """
        SELECT 
            table_name,
            table_type,
            creation_time,
            last_modified_time
        FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
        ORDER BY last_modified_time DESC
        LIMIT 10
    """,
    
    "count_rows_by_date": """
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as row_count
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    """,
    
    "get_recent_records": """
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
        ORDER BY created_at DESC
        LIMIT 100
    """,
    
    "aggregate_metrics": """
        SELECT 
            status,
            COUNT(*) as count,
            AVG(processing_time) as avg_processing_time,
            MAX(created_at) as latest_record
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY status
        ORDER BY count DESC
    """
}