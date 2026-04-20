import pandas as pd
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, avg

# Connect via psycopg2 (already working)
conn = psycopg2.connect(
    dbname="banking_db",
    user="postgres",
    password="abhishek",
    host="localhost",
    port=5432
)

# Load data into pandas
df_pandas = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

print("Data loaded from PostgreSQL:")
print(df_pandas)

# Create Spark session (no JDBC needed)
spark = SparkSession.builder \
    .appName("BankingAnalytics") \
    .getOrCreate()

# Convert pandas DataFrame to Spark DataFrame
df_spark = spark.createDataFrame(df_pandas)
df_spark.show()

print("=== Transaction Summary by Type ===")
df_spark.groupBy("type").agg(
    count("transaction_id").alias("count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount")
).show()

spark.stop()