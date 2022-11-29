import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By



headers = {
    "Accept": "text/css,*/*;q=0.1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,uz;q=0.5,de;q=0.4",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

r = requests.get(url="https://www.olx.uz/d/rabota/samarkand/", headers=headers)
soup = BeautifulSoup(r.text, "lxml")
vacancy_links = soup.find_all('a', class_='css-rc5s2u')
job_links = []
counter = 0

for link in vacancy_links:
    job_links.append(f'https://www.olx.uz{link.get("href")}')


for link in job_links:
    url = link
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\Dean\Desktop\py_proj\1\olx_parser\chromedriver\chromedriver.exe')

    try:
        driver.get(url=link)
        coockies = driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div[3]/button/span/span')
        coockies.click()

        title = driver.find_element(By.CLASS_NAME, 'css-r9zjja-Text').text
        descr = driver.find_element(By.CLASS_NAME, 'css-1g2c8kb-Text').text
        phone_element = driver.find_element(By.CLASS_NAME, 'css-cuxnr-BaseStyles')
        time.sleep(1)
        phone_element.click()
        time.sleep(4)
        phone_number = driver.find_element(By.CSS_SELECTOR, 'a.css-v1ndtc').text

        phone_number = phone_number.replace('+', '')
        phone_number = ''.join(phone_number.split('-'))
        phone_number = ''.join(phone_number.split())
        if len(phone_number) == 9:
            phone_number = '998' + phone_number
        else:
            pass

        phone_number = '+' + phone_number

        with open('vacancy.txt', 'a', encoding='utf-8') as file:
            file.write(f'#Вакансия\n\n{title}\n\n{descr}\n\nТелефон: {phone_number}\n\n**************\n\n')

        counter += 1

        time.sleep(5)

    except Exception as ex:
        print(ex)
        continue
    finally:
        driver.close()
        driver.quit()


print(counter)