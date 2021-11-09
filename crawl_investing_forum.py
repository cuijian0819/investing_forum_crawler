from selenium import webdriver
import lxml
import time
from pdb import set_trace
from selenium.webdriver.common.by import By


i=3

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

url="https://www.investing.com/crypto/bitcoin/chat/{}".format(i)

response = driver.get(url)

show_reply_list = driver.find_elements(By.XPATH, '//a[@class="showMoreReplies"]')
while (show_reply_list!=[]):
    for show_reply in show_reply_list:
        show_reply[0].click()
    show_reply_list = driver.find_elements(By.XPATH, '//a[@class="showMoreReplies"]')

show_text_list = driver.find_elements(By.XPATH, '//span[@class="showMoreText"]') 
for show_text in show_text_list: 
    show_text.click()
    driver.implicitly_wait(5)


with open('investing_btc_{}.html'.format(i), 'w') as f:
    f.write(driver.page_source)