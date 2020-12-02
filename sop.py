from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import dbm
import time
import sys


browser = webdriver.Chrome('./chromedriver')

shopee_name = input("masukin username ente... : ")
shopee_pass = input("masukin password ente...: ")


browser.get('https://shopee.co.id/buyer/login')
time.sleep(1)


browser.find_element_by_name("loginKey").send_keys(shopee_name)
browser.find_element_by_name("password").send_keys(shopee_pass)
time.sleep(3)


browser.find_element_by_xpath(
    '//*[@id="main"]/div/div[2]/div/div/form/div/div[2]/button').click()
print('cek siapa tau ada captha, atau masukin OTP, ente punya waktu 30 Detik, kalo gagal ctrl c, dan ente ulangi atau disable autentikasi dua faktor')
time.sleep(30)
print("login done..")


browser.get('https://shopee.co.id/user/purchase/list/?type=3')

time.sleep(5)
print("mengambil data checkout....")
print('lama bro klo, ente hobi belanja. ngopi aja dulu')

scroll_pause_time = 3
screen_height = browser.execute_script(
    "return window.screen.height;")
i = 1

while True:

    browser.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)

    scroll_height = browser.execute_script(
        "return document.body.scrollHeight;")

    if (screen_height) * i > scroll_height:
        break

time.sleep(5)


seller_name = browser.find_elements_by_class_name(
    'order-content__header__seller__name')
for title in seller_name:
    print(title.text)

print('DONE..')

links = browser.find_elements_by_class_name(
    'order-content__header__seller__name')
print('TOTAL CHECKOUT: ', len(links))

product_containers = browser.find_elements_by_class_name(
    'order-card__container')

seller_name = list()
total_checkout = list()

for container in product_containers:
    seller_name.append(container.find_element_by_class_name(
        'order-content__header__seller__name').text)
    total_checkout.append(
        container.find_element_by_class_name('purchase-card-buttons__total-price').text)

data = {'Nama Seller': seller_name, 'Nilai checkout': total_checkout}

df_product = pd.DataFrame.from_dict(data)

print(df_product.head())

df_product.to_csv('total_checkout.csv')


print('dah beres tuh, file disimpan dalam format total_checkout.csv, tinggal ente jumlahin aja di excel, dan jangan lupa belanja di izzabags')
