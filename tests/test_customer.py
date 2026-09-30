import allure
import pytest
from pyspark.sql.functions import col, count, when
from config.config import SOURCE_TABLE, TARGET_TABLE
from utilities.spark_utils import read_mysql_table


@allure.epic("ETL Validations")
@allure.feature("Customer Data Validation")
@allure.story("Record Count Comparison")
def test_customer_record_count(spark):
    """Validate that source and target record counts match."""
    with allure.step("1. Extract Source and Target DataFrames"):
        source_df = read_mysql_table(spark, SOURCE_TABLE)
        target_df = read_mysql_table(spark, TARGET_TABLE)

    with allure.step("2. Calculate Row Counts"):
        source_count = source_df.count()
        target_count = target_df.count()

    with allure.step("3. Assert Source and Target Row Counts Match"):
        assert source_count == target_count, (
            f"Record count mismatch! Source: {source_count}, Target: {target_count}"
        )


@allure.epic("ETL Validations")
@allure.feature("Customer Data Validation")
@allure.story("Balance Column Validation")
def test_customer_amount_validation(spark):
    """Validate that the balance column matches between Source and Target tables."""
    with allure.step("1. Extract Source and Target DataFrames"):
        source_df = read_mysql_table(spark, SOURCE_TABLE)
        target_df = read_mysql_table(spark, TARGET_TABLE)

    with allure.step("2. Join Source and Target on customer_id"):
        joined_df = source_df.alias("src").join(
            target_df.alias("tgt"), on="customer_id", how="inner"
        )

    with allure.step("3. Filter Mismatched Balances"):
        mismatched_df = joined_df.filter(
            col("src.balance") != col("tgt.balance")
        ).select(
            col("customer_id"),
            col("src.customer_name").alias("name"),
            col("src.balance").alias("source_balance"),
            col("tgt.balance").alias("target_balance"),
        )
        mismatch_count = mismatched_df.count()

    with allure.step("4. Assert No Mismatches Exist"):
        assert mismatch_count == 0, (
            f"Balance validation failed! Found {mismatch_count} mismatched records."
        )


@allure.epic("ETL Validations")
@allure.feature("Customer Data Validation")
@allure.story("Null Value Check")
def test_target_null_check(spark):
    """Ensure key columns in the target table do not contain NULL values."""
    with allure.step("1. Extract Target DataFrame"):
        target_df = read_mysql_table(spark, TARGET_TABLE)

    with allure.step("2. Check for NULLs in Primary Key and Mandatory Columns"):
        # Mandatory columns that should never be NULL
        mandatory_cols = ["customer_id", "customer_name", "balance"]

        null_counts = target_df.select([
            count(when(col(c).isNull(), c)).alias(c) for c in mandatory_cols
        ]).collect()[0].asDict()

        failed_cols = {k: v for k, v in null_counts.items() if v > 0}

    with allure.step("3. Assert No Nulls Found in Key Columns"):
        assert len(failed_cols) == 0, f"NULL values detected in target table: {failed_cols}"


@allure.epic("ETL Validations")
@allure.feature("Customer Data Validation")
@allure.story("Duplicate Check")
def test_target_duplicate_records(spark):
    """Verify that there are no duplicate primary keys in the target table."""
    with allure.step("1. Extract Target DataFrame"):
        target_df = read_mysql_table(spark, TARGET_TABLE)

    with allure.step("2. Find Duplicate customer_ids"):
        duplicate_count = target_df.groupBy("customer_id") \
            .count() \
            .filter(col("count") > 1) \
            .count()

    with allure.step("3. Assert Uniqueness of Primary Key"):
        assert duplicate_count == 0, f"Found {duplicate_count} duplicate customer_id(s) in target table."


@allure.epic("ETL Validations")
@allure.feature("Customer Data Validation")
@allure.story("Schema Structure & Column Presence")
def test_schema_match(spark):
    """Validate that target schema contains all expected columns with correct names."""
    with allure.step("1. Extract Source and Target DataFrames"):
        source_df = read_mysql_table(spark, SOURCE_TABLE)
        target_df = read_mysql_table(spark, TARGET_TABLE)

    with allure.step("2. Compare Column Lists"):
        source_cols = set(source_df.columns)
        target_cols = set(target_df.columns)
        missing_in_target = source_cols - target_cols

    with allure.step("3. Assert All Source Columns Exist in Target"):
        assert len(missing_in_target) == 0, f"Target table is missing columns: {missing_in_target}"