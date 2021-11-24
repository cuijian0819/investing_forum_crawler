#!/usr/bin/env python3
import requests
import json
from pprint import pprint
import pymongo
import urllib
import pandas as pd
from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError
import sys
import time
from tqdm import tqdm
from datetime import datetime
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import gridfs
import pdb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

username = urllib.parse.quote_plus('nss')
password = urllib.parse.quote_plus('nssadmin!')
conn = pymongo.MongoClient('mongodb://%s:%s@143.248.57.12' % (username, password), 27017)

db = conn.twitter_CVE

collection = db.url
collection.create_index("id", unique=True)

fs = gridfs.GridFS(db, "url_large")

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

f = open("url.log", "a")


def get_response(url):

	response = driver.get(url)
	time.sleep(3)

	try:
		text = driver.find_element_by_tag_name('body').text
	except:
		try:
			text = driver.find_element_by_tag_name('BODY').text
		except:
			return None

	response = {"html": str(driver.page_source), "text": text}

	return response


def logging(log):
	log = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + log
	f.write(log + "\n")
	f.flush()
	print(log)


def get_html_list(url_list):
	html_list = []
	
	for url_json in url_list:
		response = get_response(url_json["expanded_url"])

		if response:
			html_list.append({"url": url_json["url"], "expaned_url": url_json["expanded_url"], "html": response["html"], "text": response["text"]})

	return html_list


def get_size(obj, seen=None):
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	
	obj_id = id(obj)
	if obj_id in seen:
		return 0

	seen.add(obj_id)
	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for k in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum([get_size(i, seen) for i in obj])
	return size


index = int(sys.argv[2])

json_file = open(sys.argv[1])
json_list = json.load(json_file)

cnt = cnt = index - 1
total = len(json_list)

for item in json_list[index - 1:]:
	cnt += 1
	tweet_id = int(item["id"])
	name = item["user"]["screen_name"]
	url_list = item["entities"]["urls"]

	if collection.find_one({"id": tweet_id}):
		logging("[{}/{}] {} {} dup skip".format(cnt, total, tweet_id, name))
		continue

	if fs.exists({"id": tweet_id}):
		logging("[{}/{}] {} {} dup large skip".format(cnt, total, tweet_id, name))
		continue

	try:
		html_list = get_html_list(url_list)
	except:
		traceback.print_exc()
		driver.close()
		exit()


	document = {"id": tweet_id, "id_str": str(tweet_id), "screen_name": name, "urls": html_list}

	size = get_size(document)

	if size > 16*1024*1024:
		fs.put(json.dumps(document), id=tweet_id, id_str=str(tweet_id), screen_name=name, encoding="utf-8")
		logging("[{}/{}] {} {} {}/{} urls large".format(cnt, total, tweet_id, name, len(html_list), len(url_list)))
	else:
		try:
			collection.insert_one(document)
			logging("[{}/{}] {} {} {}/{} urls".format(cnt, total, tweet_id, name, len(html_list), len(url_list)))
		except DuplicateKeyError:
			logging("[{}/{}] {} {} dup error".format(cnt, total, tweet_id, name))

driver.close()
exit(10)