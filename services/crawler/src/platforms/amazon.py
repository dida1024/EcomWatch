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
            print(f"Searching for {keyword_arg} on page {page}")
            time.sleep(10)  # 等待页面加载
            elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')

            for element in elements:
                product_info = self.get_product_info(element)
                print(product_info)
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
        
        # 定义可能的标题选择器
        title_selectors = [
            'span.a-size-base-plus.a-color-base.a-text-normal',
            'span.a-size-medium.a-color-base.a-text-normal',  # 保留旧选择器作为备选
            # 'span.a-text-normal'  # 更宽松的选择器
        ]
        
        try:
            a_tag = element.find_element(By.TAG_NAME, 'a')
            
            # 尝试不同的选择器
            for selector in title_selectors:
                try:
                    product_title = element.find_element(By.CSS_SELECTOR, selector)
                    if product_title:
                        break
                except:
                    continue
                
            if not product_title:
                print("无法找到商品标题")
                return None
                
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