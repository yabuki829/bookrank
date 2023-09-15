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



# urlから本のタイトルを取得する
def scrape_amazon_title(url):
    current_path = os.path.abspath(os.path.dirname(__file__))

    # chromedriverのローカルの相対パスを作成
    chrome_driver_path = os.path.join(current_path, 'chromedriver-mac-x64', 'chromedriver')

    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        driver.get(url)
        title_element = driver.find_element_by_id('productTitle')
        title = title_element.text.strip()
        
    except NoSuchElementException:
        print("Error: Couldn't find the element with ID 'productTitle'.")
        return "NoSuchElementException"
    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        return None
    finally:
        # エラーの有無に関係なく、ドライバーを終了させる
        driver.quit()

    return title