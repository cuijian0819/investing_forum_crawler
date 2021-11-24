from tqdm import tqdm
import os
from bs4 import BeautifulSoup
from lxml import etree
from pdb import set_trace
import pickle
import pandas as pd
import requests


with open("data/parsed/investing_posts_dict", "rb") as f:
    posts_dict = pickle.load(f)

df = pd.DataFrame(posts_dict.values())


if not os.path.exists('data/user_prof'):
    os.mkdir('data/user_prof')

    
poster_url_list = df['poster_url'].tolist()
base_url = 'https://www.investing.com'
poster_id_set = set()
for poster_url in tqdm(poster_url_list):
    url = base_url + poster_url
    print(url)
    poster_id = poster_url.split('/')[-1]
    if poster_id in poster_id_set: continue;
    poster_id_set.add(poster_id)
    r = requests.get(url)
    while r.status_code == 503:
        print("status code 503, sleep...")
        time.sleep(20)
        r = requests.get(url)
    content = r.text

    with open('data/user_prof/{}.html'.format(poster_id), 'w') as f:
        f.write(content)

    break