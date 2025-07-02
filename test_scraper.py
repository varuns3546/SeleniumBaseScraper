import os
from seleniumbase import BaseCase
import sqlite3
import json

class Scraper(BaseCase):
    def test_get_links(self):
        page_number = 1
        #query_id = int(os.environ.get("QUERY_ID"))
        with open("config.json", "r") as f:
            config = json.load(f)

        query_id = int(config.get("QUERY_ID"))
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT query_type_id, title, parameters_json FROM queries WHERE id = ?", (query_id,))
        query_data = cursor.fetchone()
        conn.close()

        query_type_id = query_data[0]
        title = query_data[1]
        parameters_json = query_data[2]

        params = json.loads(parameters_json)
        pagination = params.get("pagination", "url")
        sleep_time = float(params.get("sleep_time", 1))  
        url = params.get("url")
        item_selector = params.get("item_selector")
        pagination_button_selector = params.get("pagination_button_selector")

        items = []
        if pagination =="url": 
            self.open(url.replace("*", str(page_number)))
        else:
            self.open(url)
        while True:
            self.sleep(sleep_time)
            elements = self.find_elements(item_selector)
            if not elements:
                break

            last_new_element = None
            for i, e in enumerate(elements, start=1):
                href = e.get_attribute("href")
                title = e.text
                if href and all(href != item['url'] for item in items):
                    items.append({"title": title, "url": href})
                    last_new_element = e
                print(f"{i}. {title}")

            if last_new_element:
                try:
                    self.execute_script("arguments[0].scrollIntoView(true);", last_new_element)
                except Exception as e:
                    print(f"Scroll error: {e}")
            else:
                try:
                    page_number += 1
                    if pagination =="url": 
                        self.open(url.replace("*", str(page_number)))
                    elif pagination_button_selector: 
                        self.click(pagination_button_selector)
                    else:
                        self.open(url)
                    self.sleep(sleep_time*2)
                except Exception as e:
                    print(f"No more pages or failed to open next page: {e}")
                    break

        print(f"{len(items)} links found")
        self.save_data(query_id, items)
    
    def save_data(self, query_id, items):
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        
        for item in items:
            cursor.execute('''
                INSERT INTO items (query_id, title, url)
                VALUES (?, ?, ?)
            ''', (query_id, item['title'], item['url']))
        
        conn.commit()
        conn.close()
