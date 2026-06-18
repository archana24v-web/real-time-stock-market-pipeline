from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, schema_of_json, to_timestamp, round as spark_round
from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType

spark = SparkSession.builder \
    .appName("SilverTransform") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

BRONZE_PATH = "abfss://bronze@youradls.dfs.core.windows.net/stock_ticks/"
SILVER_PATH = "abfss://silver@youradls.dfs.core.windows.net/stock_ticks_clean/"

STOCK_SCHEMA = StructType([
    StructField("symbol", StringType()),
    StructField("timestamp", StringType()),
    StructField("open", FloatType()),
    StructField("high", FloatType()),
    StructField("low", FloatType()),
    StructField("close", FloatType()),
    StructField("volume", LongType())
])

bronze_df = spark.read.format("delta").load(BRONZE_PATH)

silver_df = bronze_df \
    .withColumn("timestamp", to_timestamp(col("timestamp"))) \
    .filter(col("close") > 0) \
    .filter(col("volume") > 0) \
    .dropDuplicates(["symbol", "timestamp"]) \
    .withColumn("close", spark_round(col("close"), 2))

silver_df.write.format("delta").mode("overwrite").save(SILVER_PATH)
print(f"Silver layer written: {silver_df.count()} records")
