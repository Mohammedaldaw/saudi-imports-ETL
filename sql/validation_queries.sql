-- Check total rows loaded
SELECT count(*) FROM imports_staging;

-- Find top 5 countries by import value in 2025
SELECT country, sum(import_value) as total_value
FROM imports_staging
WHERE year = 2025
GROUP BY country
ORDER BY total_value DESC
LIMIT 5;

-- Check for data quality issues (Null values)
SELECT * FROM imports_staging
WHERE year IS NULL OR import_value IS NULL;