CREATE TABLE IF NOT EXISTS imports_staging (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    quarter VARCHAR(5) NOT NULL,
    country VARCHAR(100),
    commodity_code VARCHAR(50),
    import_value DECIMAL(20, 2),
    weight_kg DECIMAL(20, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);