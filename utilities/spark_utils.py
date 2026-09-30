import sys
from pathlib import Path
from pyspark.sql import SparkSession

# Add the project root to sys.path so config can be imported reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import config directly
import config.config as config


def create_spark_session():
    """Creates and returns a SparkSession with MySQL JDBC driver attached."""
    spark = (
        SparkSession.builder
        .appName("Customer ETL Pytest Framework")
        .master("local[*]")
        .config("spark.jars.packages", "com.mysql:mysql-connector-j:9.4.0")
        .getOrCreate()
    )
    return spark


def read_mysql_table(spark, table_name):
    """Reads data from a MySQL table into a PySpark DataFrame."""
    df = (
        spark.read
        .format("jdbc")
        .option("url", config.MYSQL_JDBC_URL)
        .option("dbtable", table_name)
        .option("user", config.MYSQL_USER)
        .option("password", config.MYSQL_PASSWORD)
        .option("driver", config.MYSQL_DRIVER)
        .load()
    )
    return df
