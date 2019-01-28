#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:48:26 2019

This documents the code I used to scrape Google Images with Selenium

@author: dbeskow
"""

import os
import re
import time
import argparse
import requests
import io
import hashlib
import itertools
import base64
from PIL import Image
from multiprocessing import Pool
from selenium import webdriver

#%%
def persist_image(dir_image_src):
    label_directory = dir_image_src[0]
    image_src = dir_image_src[1]

    size = (200, 200)
    try:
        image_content = requests.get(image_src).content
    except requests.exceptions.InvalidSchema:
        # image is probably base64 encoded
        image_data = re.sub('^data:image/.+;base64,', '', image_src)
        image_content = base64.b64decode(image_data)
    except Exception as e:
        print("could not read", e, image_src)
        return False

    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    with open('graphs/' + hashlib.sha1(image_content).hexdigest() + ".jpg", 'wb')  as h:
        image.save(h, "JPEG", quality=85)
    resized = image.resize(size)
    with open(label_directory + hashlib.sha1(image_content).hexdigest() + ".jpg", 'wb')  as f:
        resized.save(f, "JPEG", quality=85)

    return True

#%%
# The method below is a bit manual (meaning it requires the user to scroll down), but was adequate
# for my needs since I only had a few queries.  It wouldn't be hard to automate the scrolling if you
# have hundreds of queries
query = 'memes'

image_urls = set()

search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

browser = webdriver.Chrome('C:/Users/dmbes/Downloads/chromedriver_win32/chromedriver.exe')

browser.get(search_url.format(q=query))

## Now scroll down to bottom of file

images = browser.find_elements_by_css_selector("img.rg_ic")
for img in images:
    image_urls.add(img.get_attribute('src'))
    

#%%
query_directory = './img/'

values = [item for item in zip(itertools.cycle([query_directory]), image_urls)]

print("image count", len(image_urls))


for image in values:
    persist_image(image)
    
browser.quit()