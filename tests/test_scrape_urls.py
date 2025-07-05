import os
from seleniumbase import BaseCase
from pymongo import MongoClient, UpdateOne

class Scraper(BaseCase):
    def test_scrape_urls(self):
        print('hello world')
        try:
    # Connect to MongoDB
            client = MongoClient(os.getenv("MONGODB_URI"))
            db = client["amazon_best_sellers_home_and_kitchen"]
            
            # Access collections
            items_collection = db["items"]
            selectors_collection = db["selectors"]

            # Fetch selectors
            selectors = list(selectors_collection.find())

            # Print selectors
            print("Connected successfully. Selectors found:")
            for selector in selectors:
                print(selector)

        except Exception as e:
            print("Connection failed or error during retrieval:", str(e))
    
        bulk_updates = []



        for index, item in enumerate(items_collection.find(), 1):
            self.open(item['url'])
            print('url '+ item['url'])

            updates = {}

            for selector_doc in selectors:
                for title, selector in selector_doc.items():
                    if title == "_id":
                            continue
                    try:
                        text = self.find_element(selector).text.strip()
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

        