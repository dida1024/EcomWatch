from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class AmazonCrawler:
    def __init__(self, driver_arg):
        self.driver = driver_arg

    @staticmethod
    def search(keyword_arg):
        search_url = f"https://www.amazon.com/s?k={keyword_arg.replace(' ', '+')}&s=exact-aware-popularity-rank&page={{}}"
        return search_url

    def get_products(self, keyword_arg, pages=20):
        all_products = []
        search_url = self.search(keyword_arg)

        for page in range(1, pages + 1):
            self.driver.get(search_url.format(page))
            time.sleep(2)  # 等待页面加载
            elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')

            for element in elements:
                product_info = self.get_product_info(element)
                if product_info:
                    all_products.append(product_info)

            print(f'Page {page} completed: Found {len(elements)} products.')

        return all_products

    @staticmethod
    def get_product_info(element):
        product_title = None
        star = None
        reviews_count = None
        a_tag = None
        try:
            a_tag = element.find_element(By.TAG_NAME, 'a')
            product_title = element.find_element(By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal')
            star = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'i.a-icon-star-small span.a-icon-alt'))
            )
            reviews_count = element.find_element(By.CSS_SELECTOR, 'span.a-size-base.s-underline-text')
            price = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price span.a-offscreen"))
            ).get_attribute("innerHTML")
        except TimeoutException:
            price = "N/A"

        return {
            'title': product_title.text,
            'link': a_tag.get_attribute("href"),
            'price': price,
            'reviews': reviews_count.text if reviews_count else "N/A",
            'star': star.get_attribute("innerHTML") if star else "N/A",
        }


if __name__ == '__main__':
    chrome_options = Options()
    # Uncomment for headless mode
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = webdriver.Chrome(options=chrome_options)

    amz_crawler = AmazonCrawler(driver)
    keyword = "gaming keyboard"
    products = amz_crawler.get_products(keyword, pages=20)

    for product in products:
        print(f'Title: {product["title"]}')
        print(f'Link: {product["link"]}')
        print(f'Price: {product["price"]}')
        print(f'Reviews: {product["reviews"]}')
        print(f'Star: {product["star"]}')
        print('-' * 40)

    driver.quit()
