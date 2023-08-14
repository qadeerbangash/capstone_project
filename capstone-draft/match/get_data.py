import redis
import json
from decouple import config

def get_redis(val):
    redis_host = config('REDIS_HOST')
    redis_port = config('REDIS_PORT')
    redis_client = redis.Redis(host=redis_host, port=redis_port)
    specialization_keys = redis_client.keys("specialization:*")
    
    for key in specialization_keys:
        specialization = key.decode().split(":")[1]
        if specialization == val:
            data_from_redis = redis_client.get(key)

            if data_from_redis is not None:
                try:
                    records = json.loads(data_from_redis)
                    top_records=records[:10]
                    result = [{"councillor_id": item["councillor_id"]} for item in top_records]
                    

                    # `records` will contain the array of objects
                    print("Retrieved table data from Redis for specialization", specialization)
                    return result
                except json.JSONDecodeError:
                    print("Error decoding JSON data from Redis")
            else:
                print("Table data not found in Redis for specialization", specialization)
        
    redis_client.close()