import os
from seleniumbase import BaseCase

class Scraper(BaseCase):
    def test_get_links(self):
        SLEEP_TIME = 1.5
        page_number = 1

        template = os.environ.get("URL_TEMPLATE")
        if not template:
            print("Invalid or missing URL template.")
            return

        links = []
        url = template.replace("*", str(page_number))
        self.open(url)
        while True:
            self.sleep(SLEEP_TIME)
            elements = self.find_elements('a.a-link-normal.aok-block')
            if not elements:
                break

            last_new_element = None
            for i, e in enumerate(elements, start=1):
                href = e.get_attribute("href")
                if href and href not in links:
                    links.append(href)
                    last_new_element = e
                print(f"{i}. {href}")

            if last_new_element:
                try:
                    self.execute_script("arguments[0].scrollIntoView(true);", last_new_element)
                except Exception as e:
                    print(f"Scroll error: {e}")
            else:
                try:
                    page_number += 1
                    self.open(template.format(page_number, page_number))
                    self.sleep(SLEEP_TIME)
                except Exception as e:
                    print(f"No more pages or failed to open next page: {e}")
                    break

        print(f"{len(links)} links found")
