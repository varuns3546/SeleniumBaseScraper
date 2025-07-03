import os
from seleniumbase import BaseCase
from pymongo import MongoClient, UpdateOne

class Scraper(BaseCase):
    def test_scrape_urls(self):
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["amazon_best_sellers_home_and_kitchen"]
        items_collection = db["items"]
        selectors = list(db["selectors"].find())
    
        bulk_updates = []



        for index, item in enumerate(items_collection.find(), 1):
            self.open(item['url'])

            updates = {}

            for selector_doc in selectors:
                for title, selector in selector_doc.items():
                    if title == "_id":
                            continue
                    try:
                        text = self.find_element(selector).text
                        print(text)
                        updates[title] = text
                    except Exception as e:
                        print(f"Error extracting '{title}' using selector '{selector}': {e}")
                
            bulk_updates.append(
                UpdateOne({"_id": item["_id"]}, {"$set": updates})
            )

            if len(bulk_updates) == 10:
                items_collection.bulk_write(bulk_updates)
                print("Updated 10 documents")
                bulk_updates = []

        if bulk_updates:
            items_collection.bulk_write(bulk_updates)
            print(f"Updated remaining {len(bulk_updates)} documents")

        