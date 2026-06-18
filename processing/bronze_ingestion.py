from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder \
    .appName("BronzeIngestion") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

KAFKA_BOOTSTRAP = "localhost:9092"
BRONZE_PATH = "abfss://bronze@youradls.dfs.core.windows.net/stock_ticks/"

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
    .option("subscribe", "stock_ticks") \
    .load()

df_with_meta = df.withColumn("ingested_at", current_timestamp())

df_with_meta.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", BRONZE_PATH + "_checkpoint") \
    .start(BRONZE_PATH)

spark.streams.awaitAnyTermination()
