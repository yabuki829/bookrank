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
def scrape_amazon_title_and_isbn(url):
    current_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver_path = os.path.join(current_path, 'chromedriver-mac-x64', 'chromedriver')

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled') 

        driver = webdriver.Chrome(executable_path=chrome_driver_path,options=options)
        # driver = webdriver.Chrome(executable_path=chrome_driver_path)
        driver.get(url)
        time.sleep(random.random() * 4)           
        # time.sleep(100)    
        driver.execute_script('window.scrollTo(0, 1000);')
        time.sleep(random.random() * 8)           
        driver.execute_script('window.scrollTo(0, 0);')
        time.sleep(random.random() * 8) 
        text = driver.page_source 
        soup = BeautifulSoup(text,"html.parser")

        asin = soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        print(asin)
        if asin == None :
           return [None,None]

        asin = asin.find("li").find_all("span")[2].text.strip() 

        for element_li in soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find_all("li"):
            if check_asin(element_li.find_all("span")[2].text.strip()) or check_isbn(element_li.find_all("span")[2].text.strip().replace("-", "")):
                isbn =  element_li.find_all("span")[2].text.strip().replace("-", "")
                # driver.quit()
                print(isbn)


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
            return [None,None]
        
    except NoSuchElementException:
        print("Error: Couldn't find the required element.")
        return [None,None]
    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
        return [None,None]
    finally:
        driver.quit()

    return [title,isbn]


import time                                 # スリープを使うために必要
from selenium import webdriver    
import random 
# googleで検索する
# aタグを押してamazonのサイトに行く
# isbn取得する
# https://images-na.ssl-images-amazon.com/images/P/[asin].09.LZZZZZZZ.jpg
def scrape_isbn_for_amazon(search_word):
    search_word = 'site:https://www.amazon.co.jp ' + search_word 
    print(search_word)
    current_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver_path = os.path.join(current_path, 'chromedriver-mac-x64', 'chromedriver')
    "LC20lb"
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled') 

    driver = webdriver.Chrome(executable_path=chrome_driver_path,options=options)
    driver.get('https://www.google.com/')       
    
    search = driver.find_element_by_name('q')   
    search.send_keys(search_word)            
    search.submit()     
    time.sleep(random.random() * 4)           
    # time.sleep(100)    
    driver.execute_script('window.scrollTo(0, 1000);')
    time.sleep(random.random() * 8)           
    driver.execute_script('window.scrollTo(0, 0);')
    time.sleep(random.random() * 8) 
    e = driver.find_element_by_class_name("LC20lb")               
    e.click()

    # isbn,asinを取得する 
    text = driver.page_source 
    soup = BeautifulSoup(text,"html.parser")

    asin = soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find("li").find_all("span")[2].text.strip()

    for element_li in soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find_all("li"):

        if check_asin(element_li.find_all("span")[2].text.strip()) or check_isbn(element_li.find_all("span")[2].text.strip().replace("-", "")):
            isbn =  element_li.find_all("span")[2].text.strip().replace("-", "")
            # driver.quit()
            print("test",isbn)
            return isbn
    
    
    return None



from selenium.webdriver.common.by import By

def scrape_isbn_for_amazon_A(search_word):

    current_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver_path = os.path.join(current_path, 'chromedriver-mac-x64', 'chromedriver')
    "LC20lb"
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled') 

    driver = webdriver.Chrome(executable_path=chrome_driver_path,options=options)
    driver.get('https://www.amazon.co.jp')       
    
    # 検索ワードを入力
    element = driver.find_element_by_id("twotabsearchtextbox")
    element.send_keys(search_word)

    # 検索ボタンをクリック
    driver.find_element_by_id("nav-search-submit-button").click()
    time.sleep(random.random() * 4)           
    driver.execute_script('window.scrollTo(0, 1000);')
    time.sleep(random.random() * 8)           
    driver.execute_script('window.scrollTo(0, 0);')
    time.sleep(random.random() * 8)           
    # 一番めのしょうひんをクリックする
    # 別タブで商品詳細が表示されるから別の方法を考える

    # urlを取得してもう一度driver.getする
    element = driver.find_element_by_class_name("a-link-normal")
    
    
    URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")
    URL = URLS[0].get_attribute("href")

    driver.get(URL)       

    
    driver.execute_script('window.scrollTo(0, 800);')
    # isbn,asinを取得する 
    text = driver.page_source 
    soup = BeautifulSoup(text,"html.parser")

    asin = soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find("li").find_all("span")[2].text.strip()

    for element_li in soup.find("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find_all("li"):

        if check_asin(element_li.find_all("span")[2].text.strip()) or check_isbn(element_li.find_all("span")[2].text.strip().replace("-", "")):
            isbn =  element_li.find_all("span")[2].text.strip().replace("-", "")
            driver.quit()
            return isbn
    
    driver.quit()

    return None

def is_alphanumeric_only(s):
    return bool(re.match('^[a-zA-Z0-9]*$', s))

# isbn-13だと画像が表示されないことが多い
def check_isbn(word):
    # とりあえずこの二つを満たせばok
    # 全部数字であること　 isdigit () 
    # 13文字である　
    if word.isdigit() and len(word) == 13:
        return True
    return False

def check_asin(word):
    # 10文字であること
    # アルファベット2つ以上含まれていること
    # 数字が含まれていること
    if len(word) != 10  :
        return False

    if not is_alphanumeric_only(word) :
        return False
    # アルファベット2つ以上含まれていること
    # isbn-10を通すためにコメントアウト
    # num_alpha = sum(c.isalpha() for c in word)
    # if num_alpha < 2:
    #     return False

    # 数字が含まれていること
    if not any(c.isdigit() for c in word):
        return False
    
    return True
    

