from selenium import webdriver
# класс для указания типа селектора
from selenium.webdriver.common.by import By
# класс для ожидания наступления события
from selenium.webdriver.support.ui import WebDriverWait
# включает проверки, такие как видимость элемента на странице, доступность элемента для отклика и т.п.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import datetime


user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_option)
url = 'https://www.spaceweatherlive.com/ru/solnechnaya-aktivnost/top-50-reyting-solnechnyh-vspyshek/god/2011.html'

try:
    driver.get(url)
    # ожидаем подгрузку всех элементов тела
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
   
    page_height = driver.execute_script('return document.documentElement.scrollHeight')  # высота экрана
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == page_height:
            break
        page_height = new_height

    date_xpath = '//table[contains(@class,"table table-striped")]/tbody/tr/td[3]'
    power_xpath = '//table[contains(@class,"table table-striped")]/tbody/tr/td[2]/span'
    
    
    dates = driver.find_elements(By.XPATH, date_xpath)
    powers = driver.find_elements(By.XPATH,  power_xpath)

    rating_50 = []

    for i in range(len(dates)):
        
        # Преобразуем дату в формат datetime
        date_ = dates[i].text
        d = date_.split("/")
        date_day = datetime.date(int(d[2]), int(d[1]), int(d[0]))

        # Преобразуем данные по мощности излучения в числовой формат 
        power = powers[i].text
        if power[0] == "X":
            power = float(power[1::]) * 10
        elif power[0] == "M":
            power = float(power[1::])
        elif power[0] == "C": 
            power = float(power[1::]) / 10
        
        rating_50.append({"date": date_day, "power": power})

    with open("rating_50.csv", "w", encoding='UTF-8', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "power"])
        writer.writeheader()
        writer.writerows(rating_50)
    print('Данные сохранены в файл rating_50.csv')

except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()