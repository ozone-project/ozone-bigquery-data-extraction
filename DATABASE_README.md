# Sincera Database Documentation

## Overview
This SQLite database contains Sincera API data including ecosystem metrics and individual publisher performance data.

## Database File
- **File**: `sincera_data.db`
- **Type**: SQLite 3
- **Size**: ~XX MB
- **Last Updated**: [Date]

## Tables

### 1. `ecosystem_data`
Global Sincera ecosystem metrics and statistics.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| data_json | TEXT | Complete JSON response from /ecosystem endpoint |
| created_at | TIMESTAMP | When data was fetched |
| updated_at | TIMESTAMP | When record was last modified |

**Sample Query:**
```sql
SELECT json_extract(data_json, '$.known_adsystems') as ad_systems,
       json_extract(data_json, '$.sincera_ecosystem_size') as ecosystem_size,
       created_at
FROM ecosystem_data ORDER BY created_at DESC LIMIT 1;
```

### 2. `publisher_data`
Individual publisher metrics and performance data.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| domain | TEXT | Publisher domain (e.g., 'theguardian.com') |
| publisher_id | INTEGER | Sincera publisher ID |
| name | TEXT | Publisher display name |
| status | TEXT | Publisher status ('available', etc.) |
| primary_supply_type | TEXT | Supply type ('web', 'app', etc.) |
| pub_description | TEXT | Publisher description |
| categories | TEXT | JSON array of content categories |
| slug | TEXT | URL-friendly publisher identifier |
| avg_ads_to_content_ratio | REAL | Ratio of ads to content (0.0-1.0) |
| avg_ads_in_view | REAL | Average number of ads visible |
| avg_ad_refresh | REAL | Average ad refresh time (seconds) |
| total_unique_gpids | INTEGER | Total unique Global Publisher IDs |
| id_absorption_rate | REAL | User ID collection success rate (0.0-1.0) |
| avg_page_weight | REAL | Average page size (MB) |
| avg_cpu | REAL | Average CPU usage percentage |
| total_supply_paths | INTEGER | Number of programmatic supply paths |
| reseller_count | INTEGER | Number of reseller partners |
| owner_domain | TEXT | Parent company domain |
| raw_data_json | TEXT | Complete JSON response from /publishers endpoint |
| created_at | TIMESTAMP | When data was fetched |
| updated_at | TIMESTAMP | When record was last modified |

**Sample Queries:**
```sql
-- Top publishers by ID absorption rate
SELECT domain, name, id_absorption_rate, avg_cpu 
FROM publisher_data 
WHERE id_absorption_rate IS NOT NULL 
ORDER BY id_absorption_rate DESC;

-- Publishers with high ad density
SELECT domain, name, avg_ads_to_content_ratio, avg_ads_in_view
FROM publisher_data 
WHERE avg_ads_to_content_ratio > 0.2
ORDER BY avg_ads_to_content_ratio DESC;

-- Technical performance comparison
SELECT domain, name, avg_page_weight, avg_cpu, total_supply_paths
FROM publisher_data 
ORDER BY avg_cpu ASC;
```

### 3. `publisher_metrics`
Saved analysis summaries and statistical breakdowns.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| analysis_name | TEXT | Name of the analysis |
| publisher_count | INTEGER | Number of publishers in analysis |
| summary_stats | TEXT | JSON with statistical summaries |
| created_at | TIMESTAMP | When analysis was performed |

**Sample Query:**
```sql
SELECT analysis_name, publisher_count, created_at
FROM publisher_metrics
ORDER BY created_at DESC;
```

## Key Metrics Explained

### ID Absorption Rate
- **Definition**: Percentage of ad requests that successfully obtain a user identifier
- **Range**: 0.0 (0%) to 1.0 (100%)
- **Good**: >0.7 (70%)
- **Excellent**: >0.9 (90%)

### Ads to Content Ratio
- **Definition**: Proportion of page elements that are advertisements
- **Range**: 0.0 (no ads) to 1.0 (all ads)
- **Typical**: 0.1-0.3 (10%-30%)

### Supply Paths & Resellers
- **Supply Paths**: Number of programmatic advertising routes
- **Resellers**: Number of intermediary partners
- **More paths/resellers** = More complex monetization but potentially higher fill rates

## Connection Methods

### 1. SQLite Command Line
```bash
sqlite3 sincera_data.db
.tables
.schema publisher_data
SELECT * FROM publisher_data LIMIT 5;
```

### 2. Python
```python
import sqlite3
import json

conn = sqlite3.connect('sincera_data.db')
cursor = conn.cursor()

# Query publishers
cursor.execute("SELECT domain, name, id_absorption_rate FROM publisher_data ORDER BY id_absorption_rate DESC")
results = cursor.fetchall()

for domain, name, rate in results:
    print(f"{domain}: {name} - {rate:.1%}")

conn.close()
```

### 3. DB Browser for SQLite (GUI)
Download from: https://sqlitebrowser.org/

### 4. Online SQLite Viewers
- Upload to: https://sqliteviewer.app/
- Or: https://inloop.github.io/sqlite-viewer/

## Data Sources
- **Sincera API**: https://open.sincera.io/api/
- **Endpoint Coverage**:
  - `/ecosystem` - Global metrics
  - `/publishers?domain=X` - Individual publisher data
- **Update Frequency**: Manual/on-demand
- **Data Date Range**: [Insert date range]

## Sample Analysis Queries

### Publisher Performance Ranking
```sql
SELECT 
    domain,
    name,
    id_absorption_rate,
    avg_ads_to_content_ratio,
    avg_cpu,
    total_supply_paths,
    CASE 
        WHEN id_absorption_rate > 0.8 THEN 'Excellent'
        WHEN id_absorption_rate > 0.6 THEN 'Good'
        WHEN id_absorption_rate > 0.4 THEN 'Average'
        ELSE 'Poor'
    END as id_performance
FROM publisher_data
WHERE id_absorption_rate IS NOT NULL
ORDER BY id_absorption_rate DESC;
```

### Resource Efficiency Analysis
```sql
SELECT 
    domain,
    name,
    avg_cpu,
    avg_page_weight,
    total_supply_paths,
    reseller_count,
    ROUND(avg_cpu / avg_page_weight, 2) as cpu_per_mb
FROM publisher_data
WHERE avg_cpu > 0 AND avg_page_weight > 0
ORDER BY cpu_per_mb ASC;
```

## Contact
For questions about this database or the underlying data, contact [Your Contact Info].

## License
[Specify data usage rights and restrictions]