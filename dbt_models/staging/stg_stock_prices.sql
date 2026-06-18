-- Staging model: clean raw stock prices from Silver layer
{{ config(materialized='view') }}

SELECT
    symbol,
    timestamp,
    open,
    high,
    low,
    close,
    volume,
    ingested_at
FROM {{ source('silver', 'stock_ticks_clean') }}
WHERE close > 0
  AND volume > 0
