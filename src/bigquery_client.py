from typing import List, Dict, Any, Optional
from google.cloud import bigquery
import os


class BigQueryClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
        
        self.client = bigquery.Client(project=self.project_id)
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a BigQuery SQL query and return the results as a list of dictionaries."""
        try:
            if parameters:
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter(key, "STRING", value)
                        for key, value in parameters.items()
                    ]
                )
                query_job = self.client.query(query, job_config=job_config)
            else:
                query_job = self.client.query(query)
            
            results = []
            for row in query_job:
                results.append(dict(row))
            
            return results
        
        except Exception as e:
            raise Exception(f"BigQuery execution error: {str(e)}")
    
    def get_table_schema(self, dataset_id: str, table_id: str) -> List[Dict[str, Any]]:
        """Get the schema of a BigQuery table."""
        try:
            table_ref = self.client.dataset(dataset_id).table(table_id)
            table = self.client.get_table(table_ref)
            
            schema = []
            for field in table.schema:
                schema.append({
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description
                })
            
            return schema
        
        except Exception as e:
            raise Exception(f"Schema retrieval error: {str(e)}")
    
    def list_datasets(self) -> List[str]:
        """List all datasets in the project."""
        try:
            datasets = list(self.client.list_datasets())
            return [dataset.dataset_id for dataset in datasets]
        
        except Exception as e:
            raise Exception(f"Dataset listing error: {str(e)}")
    
    def list_tables(self, dataset_id: str) -> List[str]:
        """List all tables in a dataset."""
        try:
            dataset_ref = self.client.dataset(dataset_id)
            tables = list(self.client.list_tables(dataset_ref))
            return [table.table_id for table in tables]
        
        except Exception as e:
            raise Exception(f"Table listing error: {str(e)}")