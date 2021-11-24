from selenium import webdriver
import lxml
import time
from pdb import set_trace
from selenium.webdriver.common.by import By
import os
from tqdm import tqdm

# profile = webdriver.FirefoxProfile()
# profile.set_preference("dom.disable_open_during_load", False)
# driver = webdriver.Firefox(firefox_profile=profile, executable_path=os.getcwd()+"/geckodriver")
driver = webdriver.Firefox(executable_path=os.getcwd()+"/geckodriver")
# driver = webdriver.Chrome("./chromedriver")

crawled_page = set()
for fname in os.listdir('data/raw/'):
    crawled_page.add(int(fname.split('.')[0].split('_')[-1]))

page_to_crawl = set(range(6961)) - crawled_page
page_to_crawl = list(page_to_crawl)
page_to_crawl.sort()

for i in tqdm(list(page_to_crawl)):
    url="https://www.investing.com/crypto/bitcoin/chat/{}".format(i)

    response = driver.get(url)
    driver.implicitly_wait(10)

    # close popup window
    try:
        driver.find_elements(By.XPATH, '//i[@class="popupCloseIcon largeBannerCloser"]')[0].click()
    except:
        pass;
        # print("no popup")

    # show prev replies
    show_reply_list = driver.find_elements(By.XPATH, '//a[@class="showMoreReplies"]')
    while (show_reply_list!=[]):
        for show_reply in show_reply_list:
            try:
                show_reply.click()
                driver.implicitly_wait(5)
            except:
                driver.find_elements(By.XPATH, '//i[@class="popupCloseIcon largeBannerCloser"]')[0].click()
                show_reply.click()
                driver.implicitly_wait(5)

        show_reply_list = driver.find_elements(By.XPATH, '//a[@class="showMoreReplies"]')
        
    driver.execute_script("scrollBy(0,220);")
    # show more 
    show_text_list = driver.find_elements(By.XPATH, '//span[@class="showMoreText"]') 
    for show_text in show_text_list: 
        try:
           show_text.click()  
           driver.implicitly_wait(5)
        except:
           try:
               driver.find_elements(By.XPATH, '//i[@class="popupCloseIcon largeBannerCloser"]')[0].click()
               show_reply.click()
               driver.implicitly_wait(5)
           except: 
               driver.execute_script("scrollBy(0,220);")
               show_text.click()  
               driver.implicitly_wait(5)

    with open('data/raw/investing_btc_{}.html'.format(i), 'w') as f:
        f.write(driver.page_source)


