"""
Example usage of the BigQuery Data Extraction API.
"""

import requests
import json


class BigQueryAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def execute_query(self, query: str, parameters: dict = None):
        """Execute a BigQuery SQL query via the API"""
        url = f"{self.base_url}/query"
        payload = {"query": query}
        if parameters:
            payload["parameters"] = parameters
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_datasets(self):
        """List all datasets"""
        url = f"{self.base_url}/datasets"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def list_tables(self, dataset_id: str):
        """List tables in a dataset"""
        url = f"{self.base_url}/datasets/{dataset_id}/tables"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_table_schema(self, dataset_id: str, table_id: str):
        """Get table schema"""
        url = f"{self.base_url}/datasets/{dataset_id}/tables/{table_id}/schema"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def health_check(self):
        """Check API health"""
        url = f"{self.base_url}/health"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = BigQueryAPIClient()
    
    # Health check
    print("Health check:", client.health_check())
    
    # List datasets
    datasets = client.list_datasets()
    print(f"Found {len(datasets['datasets'])} datasets")
    
    # Example query
    sample_query = """
        SELECT 
            table_name,
            table_type,
            creation_time
        FROM `your-project.your-dataset.INFORMATION_SCHEMA.TABLES`
        LIMIT 5
    """
    
    try:
        results = client.execute_query(sample_query)
        print(f"Query returned {results['row_count']} rows")
        print(json.dumps(results['data'], indent=2))
    except Exception as e:
        print(f"Query failed: {e}")