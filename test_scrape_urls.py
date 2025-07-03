import os
from seleniumbase import BaseCase
from pymongo import MongoClient

class Scraper(BaseCase):
    def test_scrape_urls(self):
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["amazon_best_sellers_home_and_kitchen"]
        items_collection = db["items"]
        selectors = list(db["selectors"].find())
    

        for item in items_collection.find():
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
                        updates[title] = None  # or log the error
                        print(f"Error extracting '{title}' using selector '{selector}': {e}")
                
            items_collection.update_one(
                {"_id": item["_id"]},
                {"$set": updates}
            )
                

        