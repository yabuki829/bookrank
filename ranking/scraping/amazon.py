import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# URLを探す
def find_amazon_url(description):
    pattern = r"https://amzn\.to/[^\s]+"
    match = re.findall(pattern, description)
    return match if match else None

from bs4 import BeautifulSoup

# urlから本のタイトルを取得する
def scrape_amazon_title(url):
    current_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver_path = os.path.join(current_path, 'chromedriver-mac-x64', 'chromedriver')

    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        driver.get(url)

        text = driver.page_source 
        soup = BeautifulSoup(text,"html.parser")
        product = soup.find(id="productTitle")

        # 本であれば必ずどちらかがあるのでこれで本かどうかを判別
        isBook_1 = soup.find(id="rpi-attribute-book_details-fiona_pages")
        isBook_2 = soup.find(id="rpi-attribute-book_details-ebook_pages")

        isBook_3 = soup.find(id="rpi-attribute-book_details-publisher")

        if (isBook_1 or isBook_2) or isBook_3: 
            title_element = driver.find_element_by_id('productTitle')
            title = title_element.text.strip()
            print(title)
        else :
            print("本ではありません")
            return None
        
    except NoSuchElementException:
        print("Error: Couldn't find the required element.")
        return "NoSuchElementException"
    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        return None
    finally:
        driver.quit()

    return title
