import logging

from load import load_in_redis
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, desc
from tqdm import tqdm


def extract_transform(rating, appointment, patient_councillor, councillor):
    """
    Extracts data from different sources, performs transformation, and loads the transformed data into Redis.
    Returns:
        None
    """

    spark = SparkSession.builder.getOrCreate()

    rating = spark.createDataFrame(tqdm(rating, desc="Ratings"))
    appointment = spark.createDataFrame(tqdm(appointment, desc="Appointments"))
    patient_councillor = spark.createDataFrame(
        tqdm(patient_councillor, desc="Patient Councillor")
    )
    councillor = spark.createDataFrame(tqdm(councillor, desc="Councillor"))

    joined_df = (
        rating.join(appointment, rating["appointment_id"] == appointment["id"])
        .join(
            patient_councillor,
            patient_councillor["patient_id"] == appointment["patient_id"],
        )
        .join(councillor, councillor["id"] == patient_councillor["councillor_id"])
    )

    grouped_df = (
        joined_df.groupBy("councillor_id", "specialization")
        .agg(avg("value").alias("points"))
        .orderBy(desc("points"))
    )

    specializations = (
        grouped_df.select("specialization")
        .distinct()
        .toPandas()["specialization"]
        .tolist()
    )
    logging.info("Data Transformed Successfully")

    # filter and load in redis
    success = load_in_redis(specializations, grouped_df)
    if not success:
        logging.error("Error occurred during data loading into Redis")
        spark.stop()
        return None
    else:
        print(f"Data loaded in redis successfully {specializations}")

    # Stop the SparkSession
    spark.stop()
    return grouped_df
