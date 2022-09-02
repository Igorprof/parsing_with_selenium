from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json

service = Service('chromedriver.exe')

driver = webdriver.Chrome(service=service)

driver.get('https://scrapingclub.com/exercise/basic_login/')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@id='id_name']")))

username = driver.find_element(by=By.ID, value='id_name')
password = driver.find_element(by=By.ID, value='id_password')

username.send_keys('scrapingclub')
password.send_keys('scrapingclub')

login_btn = driver.find_element(by=By.XPATH, value="//form/button")

login_btn.click()

time.sleep(2)

driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card']")))

first_height = driver.execute_script("return document.body.scrollHeight;")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))

    new_height = driver.execute_script("return document.body.scrollHeight;")

    if new_height == first_height:
        break

    first_height = new_height


cards = driver.find_elements(by=By.CLASS_NAME, value='card')

data = []
for card in cards:
    try:
        img = 'https://scrapingclub.com' + card.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
        link = card.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        title = card.find_element(by=By.CLASS_NAME, value='card-title').text
        price = card.find_element(by=By.TAG_NAME, value='h5').text

        data.append({
            'image': img,
            'link': link,
            'title': title,
            'price': price
        })
    except Exception as e:
        pass

driver.quit()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

