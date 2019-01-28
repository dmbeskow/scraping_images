# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 11:43:06 2017

@author: dmbes
"""

'''
This code assumes you have a basic Twitter JSON file or directory, and will 
get all links and then images share in these tweets.

'''

import json
import io, gzip, os
import urllib.request 
import random
from random import shuffle
import codecs
import progressbar

import os, gzip, io, json
files = os.listdir()
shuffle(files)
files = os.listdir('timeline')
files = ['timeline/' + x for x in files]
links = []
for file in files:
    with io.TextIOWrapper(gzip.open(file, 'r')) as infile:
        for line in infile:
            if line != '\n':
                tweet = json.loads(line)
                if 'possibly_sensitive' in tweet.keys():
                    if tweet['possibly_sensitive']:
                        continue
                if 'media' in tweet['entities'].keys():
                    for pic in tweet['entities']['media']:
                        if pic['type'] == 'photo':
                            u = pic['media_url']
                            links.append((u,tweet['id_str']))
print('number of links',len(links)) 

#%%

'''
This will multiprocess the download (much faster)
'''

import multiprocessing
import random

def download_link(link, ID):
    u = link
    Type = u.split('.')
    Type = Type[-1]
    Name = 'img/'+ str(ID) + '_' + str(random.randint(1000,9999))  + '.' + Type
    try:
        urllib.request.urlretrieve(u, Name)
    except:
        print('error')

cores =multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes = cores)
output = pool.starmap(download_link, links)


#%%
'''
This will download in a single process (slower)
'''
count = 0
for file in files:
    with io.TextIOWrapper(gzip.open(file, 'r')) as infile:
        for line in infile:
            tweet = json.loads(line)
            if 'possibly_sensitive' in tweet.keys():
                if tweet['possibly_sensitive']:
                    count += 1
print(count)