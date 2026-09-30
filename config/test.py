# ============================================================
# MYSQL CONNECTION TEST USING PYSPARK
# ============================================================

from pyspark.sql import SparkSession

from config import (
    MYSQL_JDBC_URL,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DRIVER,
    SOURCE_TABLE,
    TARGET_TABLE
)


# ============================================================
# 1. CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("MySQL Connection Test")
    .master("local[*]")
    .config(
        "spark.jars",
        r"C:\Users\Plabani\Downloads\mysql-connector-j-9.4.0.jar"
    )
    .getOrCreate()
)


# ============================================================
# 2. TEST SOURCE TABLE
# ============================================================

print("\n==========================================")
print("TESTING SOURCE TABLE")
print("==========================================")

source_df = (
    spark.read
    .format("jdbc")
    .option("url", MYSQL_JDBC_URL)
    .option("dbtable", SOURCE_TABLE)
    .option("user", MYSQL_USER)
    .option("password", MYSQL_PASSWORD)
    .option("driver", MYSQL_DRIVER)
    .load()
)

print("Source connection successful!")
print("Source record count:", source_df.count())

source_df.show(5)


# ============================================================
# 3. TEST TARGET TABLE
# ============================================================

print("\n==========================================")
print("TESTING TARGET TABLE")
print("==========================================")

target_df = (
    spark.read
    .format("jdbc")
    .option("url", MYSQL_JDBC_URL)
    .option("dbtable", TARGET_TABLE)
    .option("user", MYSQL_USER)
    .option("password", MYSQL_PASSWORD)
    .option("driver", MYSQL_DRIVER)
    .load()
)

print("Target connection successful!")
print("Target record count:", target_df.count())

target_df.show(5)


# ============================================================
# 4. STOP SPARK
# ============================================================

spark.stop()

print("\n==========================================")
print("MYSQL CONNECTION TEST COMPLETED")
print("==========================================")