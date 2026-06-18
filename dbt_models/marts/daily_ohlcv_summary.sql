-- Gold mart: Daily OHLCV summary per stock symbol
{{ config(materialized='table') }}

SELECT
    symbol,
    DATE_TRUNC('day', timestamp) AS trade_date,
    MAX(high)                    AS daily_high,
    MIN(low)                     AS daily_low,
    AVG(close)                   AS avg_close,
    SUM(volume)                  AS total_volume
FROM {{ ref('stg_stock_prices') }}
GROUP BY symbol, DATE_TRUNC('day', timestamp)
ORDER BY trade_date DESC
