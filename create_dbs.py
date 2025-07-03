import os
import json
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["query_db"]

# Drop all existing collections
for collection_name in db.list_collection_names():
    db.drop_collection(collection_name)


# Insert into `queries`
queries_collection = db["queries"]
parameters = {
    "title": "Amazon Home and Kitchen Best Sellers",
    "url": "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_*_home-garden?_encoding=UTF8&pg=*",
    "sleep_time": "0",
    "item_selector": 'a.a-link-normal.aok-block[role="link"]:not(.a-text-normal)',
    "pagination": "url",
    "scroll_rate": "",
    "pagination_button_selector": ""
}

query_id = queries_collection.insert_one({
    "title": "Amazon Best Sellers in Home and Kitchen",
    "parameters": parameters  # No need to JSON-encode in MongoDB
}).inserted_id

# Print all collection names
print(db.list_collection_names())
