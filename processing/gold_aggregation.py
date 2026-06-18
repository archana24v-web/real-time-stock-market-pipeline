from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max as spark_max, min as spark_min, sum as spark_sum, date_trunc

spark = SparkSession.builder \
    .appName("GoldAggregation") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

SILVER_PATH = "abfss://silver@youradls.dfs.core.windows.net/stock_ticks_clean/"
GOLD_PATH = "abfss://gold@youradls.dfs.core.windows.net/daily_ohlcv_summary/"

silver_df = spark.read.format("delta").load(SILVER_PATH)

gold_df = silver_df \
    .withColumn("trade_date", date_trunc("day", col("timestamp"))) \
    .groupBy("symbol", "trade_date") \
    .agg(
        spark_max("high").alias("daily_high"),
        spark_min("low").alias("daily_low"),
        avg("close").alias("avg_close"),
        spark_sum("volume").alias("total_volume")
    )

gold_df.write.format("delta").mode("overwrite").save(GOLD_PATH)
print(f"Gold layer written: {gold_df.count()} records")
