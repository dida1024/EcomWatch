import logging
from src.platforms.base import BaseSeleniumDriver
from src.platforms.amazon import AmazonCrawler

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the keyword monitoring tool...")
    
    # 初始化Selenium WebDriver
    base_driver = BaseSeleniumDriver()
    driver = base_driver.init_driver()
    
    # 初始化亚马逊爬虫
    amz_crawler = AmazonCrawler(driver)
    
    # 获取关键词产品
    keyword = "手表"
    products = amz_crawler.get_products(keyword, pages=20)  
    
    # 打印产品信息
    for product in products:
        logger.info(f"Title: {product['title']}")
        logger.info(f"Link: {product['link']}")
        logger.info(f"Price: {product['price']}")
        logger.info(f"Reviews: {product['reviews']}")
        logger.info(f"Star: {product['star']}")
        logger.info('-' * 40)

    # 关闭Selenium WebDriver
    driver.close()

if __name__ == "__main__":
    main()
