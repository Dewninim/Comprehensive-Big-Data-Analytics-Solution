import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def rename_columns(data_source: str, output_uri: str) -> None:
    with SparkSession.builder \
        .appName("Group 13 Healthcare Dataset Analysis") \
            .getOrCreate() as spark:

        # Load CSV file
        df = spark.read.option("header", "true").csv(data_source)

        # Rename columns
        df = df.select(
            col("Name").alias("name"),
            col("Age").alias("age"),
            col("Gender").alias("gender"),
            col("Blood Type").alias("blood_type"),
            col("Medical Condition").alias("medical_condition"),
            col("Date of Admission").alias("admission_date"),
            col("Doctor").alias("doctor"),
            col("Hospital").alias("hospital"),
            col("Insurance Provider").alias("insurance_provider"),
            col("Billing Amount").alias("billing_amount"),
            col("Room Number").alias("room_number"),
            col("Admission Type").alias("admission_type"),
            col("Discharge Date").alias("discharge_date"),
            col("Medication").alias("medication"),
            col("Test Results").alias("test_results")
        )

        # Log into EMR stdout
        print(f"Number of rows after renaming columns: {df.count()}")

        # Write the output to the specified URI
        df.write.mode("overwrite").csv(output_uri)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_source", help="Input data source (e.g., HDFS or S3 path)")
    parser.add_argument(
        "--output_uri", help="Output URI (e.g., HDFS or S3 path)")
    args = parser.parse_args()

    # Call the rename_columns function
    rename_columns(args.data_source, args.output_uri)