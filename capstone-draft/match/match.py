from fastapi import FastAPI
import uvicorn
from fastapi.exceptions import HTTPException
import json
from get_data import get_redis




app = FastAPI()

@app.post("/recommend")
def create_item(item):
    try:
        json_data = json.loads(item)
        category = json_data.get('category')
        if not category:
            raise HTTPException(status_code=400, detail="Category not found in the request")
        
        print(category)
        return get_redis(category)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in the request")

# def get_redis(val):
#     config={'host':"redis",'port':6379}

#     redis_client = redis.Redis(host=config.get('host'), port=config.get('port'))
#     specialization_keys = redis_client.keys("specialization:*")
#     temp=[x.decode().split(":")[1] for x in specialization_keys]
#     print(temp)
#     # if val not in specialization_keys: raise HTTPException(status_code=404, detail="Data not found in Redis for the specified category")

#     for key in specialization_keys:
#         specialization = key.decode().split(":")[1]
#         if specialization == val:
#             data_from_redis = redis_client.get(key)

#             if data_from_redis is not None:
#                 try:
#                     records = json.loads(data_from_redis)
#                     top_records=records[:10]
#                     result = [{"councillor_id": item["councillor_id"]} for item in top_records]
                    

#                     # `records` will contain the array of objects
#                     print("Retrieved table data from Redis for specialization", specialization)
#                     return result
#                 except json.JSONDecodeError:
#                     print("Error decoding JSON data from Redis")
#                 else:
#                     print("Table data not found in Redis for specialization", specialization)
        

        
                
#     redis_client.close()

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)
    

