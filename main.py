
from seleniumbase import BaseCase

class Scraper(BaseCase):

    def test_get_links(self):
        SLEEP_TIME  = 1.5
        page_number = 1
        BASE_URL = "https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_{}_fashion?_encoding=UTF8&pg={}"


        links = []
        self.open(BASE_URL.format(page_number, page_number))
        while True:
            self.sleep(SLEEP_TIME)

            elements = self.find_elements('a.a-link-normal.aok-block')
            if not elements:
                break
            print(f"Found {len(elements)} links.")

            last_new_element = None
                        # 3) Extract and print each href
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
                    page_number +=1
                    self.open(BASE_URL.format(page_number, page_number))
                    self.sleep(SLEEP_TIME)  # give time for page navigation
                except Exception as e:
                    print(f"No more pages or failed to click 'a-last': {e}")
                    break
        print(f"{len(links)} links found")
    

if __name__ == "__main__":
    from seleniumbase import BaseCase
    BaseCase.main(__name__, __file__)
