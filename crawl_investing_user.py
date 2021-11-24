from tqdm import tqdm
import os
from bs4 import BeautifulSoup
from lxml import etree
from pdb import set_trace
import pickle
import pandas as pd
import requests
import time

# load data and convert to df
with open("data/parsed/investing_posts_dict", "rb") as f:
    posts_dict = pickle.load(f)
df = pd.DataFrame(posts_dict.values())

# make folder if not exist
if not os.path.exists('data/user_prof'):
    os.mkdir('data/user_prof')

# check crawled poster id and save into the set
poster_id_set = set()
for crawled_fname in os.listdir('data/user_prof'):
    if not 'html' in crawled_fname: continue;
    poster_id_set.add(crawled_fname.split('.')[0])
        
        

poster_url_list = df['poster_url'].unique().tolist()

base_url = 'https://www.investing.com'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for poster_url in tqdm(poster_url_list):
    # url to crawl
    url = base_url + poster_url
    
    # skip if the poster id has already crawled  
    poster_id = poster_url.split('/')[-1]
    if poster_id in poster_id_set: continue;
    
    # send request
    r = requests.get(url, headers=headers)
    while r.status_code == 403:
        print("status code 403, sleep...")
        time.sleep(20)
        r = requests.get(url)
    while r.status_code == 503:
        print("status code 503, sleep...")
        time.sleep(20)
        r = requests.get(url)
    content = r.text

    # save to file
    with open('data/user_prof/{}.html'.format(poster_id), 'w') as f:
        f.write(content)
    
    # add to crawled poster id set
    poster_id_set.add(poster_id)

