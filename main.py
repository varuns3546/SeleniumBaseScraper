from seleniumbase import BaseCase


BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_swag_labs(self):
        # Open the bestseller page
        url = "https://www.amazon.com/gp/bestsellers/fashion/ref=zg_bs_fashion_sm"
        self.open(url)

        elements = self.find_elements('a.a-link-normal.aok-block')
        print(f"Found {len(elements)} links.")

        # 3) Extract and print each href
        for i, e in enumerate(elements, start=1):
            href = e.get_attribute("href")
            print(f"{i}. {href}")