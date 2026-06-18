import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local") \
        .appName("TestSilverTransform") \
        .getOrCreate()

def test_filter_negative_close(spark):
    schema = StructType([
        StructField("symbol", StringType()),
        StructField("timestamp", StringType()),
        StructField("close", FloatType()),
        StructField("volume", LongType())
    ])
    data = [
        ("AAPL", "2026-06-17T09:30:00", 190.5, 100000),
        ("MSFT", "2026-06-17T09:30:00", -1.0, 50000),   # Bad record
        ("GOOGL", "2026-06-17T09:30:00", 175.2, 0),      # Zero volume
    ]
    df = spark.createDataFrame(data, schema)
    result = df.filter((df.close > 0) & (df.volume > 0))
    assert result.count() == 1
    assert result.collect()[0]['symbol'] == 'AAPL'
