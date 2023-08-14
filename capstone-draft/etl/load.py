# import redis 
# import json
# import logging
# from decouple import config



# def load_in_redis(specializations,grouped_df):
#     """
#     Load data into Redis for each specialization.

#     Args:
#         specializations (list): List of specialization names.
#         grouped_df (DataFrame): Spark DataFrame containing grouped data.

#     Returns:
#         None
#     """

    
    

#     redis_host = config('REDIS_HOST')
#     redis_port = config('REDIS_PORT')
#     redis_client = redis.Redis(host=redis_host, port=redis_port)



#     for specialization in specializations:
#         specialization_table = grouped_df.filter(grouped_df.specialization == specialization)
#         strip_data=specialization_table.select("councillor_id", "points")
            
            
#         records = strip_data.toPandas().to_json(orient='records')
#         records = json.dumps(json.loads(records))

            
            
        
            
#         redis_key = f"specialization:{specialization}"
#         redis_client.set(redis_key, records)
#         logging.info(f"Stored table data in Redis for specialization {specialization}")
        
#         # Close the Redis connection
#     redis_client.close()

import json
import logging

import redis  # type: ignore
from decouple import config
from redis.exceptions import RedisError  # type: ignore


def load_in_redis(specializations, grouped_df):
    """
    Load data into Redis for each specialization.

    Args:
        specializations (list): List of specialization names.
        grouped_df (DataFrame): Spark DataFrame containing grouped data.

    Returns:
        None
    """

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        redis_host = config("REDIS_HOST")
        redis_port = config("REDIS_PORT")
        redis_client = redis.Redis(host=redis_host, port=redis_port)
    except RedisError as e:
        logging.error(f"Failed to connect to Redis: {str(e)}")
        return False

    try:
        for specialization in specializations:
            specialization_table = grouped_df.filter(
                grouped_df.specialization == specialization
            )
            strip_data = specialization_table.select("councillor_id", "points")

            records = strip_data.toPandas().to_json(orient="records")
            records = json.dumps(json.loads(records))

            redis_key = f"specialization:{specialization}"
            redis_client.set(redis_key, records)
            logging.info(
                f"Stored table data in Redis for specialization {specialization}"
            )

    except RedisError as e:
        logging.error(f"Redis error occurred while loading data: {str(e)}")
        redis_client.close()
        return False

    redis_client.close()
    return True