import os
from seleniumbase import BaseCase
import sqlite3

class Scraper(BaseCase):
    def test_get_links(self):
        page_number = 1
        query_id = int(os.environ.get("QUERY_ID"))

        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute("SELECT url_template, sleep_time, item_selector, pagination, scroll_rate, " \
                    "pagination_button_selector FROM queries WHERE id = ?", (query_id,))
        result = cursor.fetchone()
        conn.close()
        url_template = result[0]
        sleep_time = result[1]
        item_selector = result[2]
        pagination = result[3]
        scroll_rate = result[4]
        pagination_button_selector = result[5]
        if not url_template:
            print("Invalid or missing URL template.")
            return

        items = []
        url = ""
        if pagination =="url": 
            url = url_template.replace("*", str(page_number))
        else: 
            url = url_template
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
                    if pagination=='url': 
                        url = url_template.replace("*", str(page_number))
                        self.open(url)
                    elif pagination_button_selector: 
                        self.click(pagination_button_selector)
                    else:
                        self.open(url_template)
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
