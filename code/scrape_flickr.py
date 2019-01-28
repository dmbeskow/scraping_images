#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:50:19 2019

@author: dbeskow
"""



#%%
import flickrapi
import urllib.request
api_key = u'XXXXXXXXXXXXXXXXXXXXXXXXX'
api_secret = u'XXXXXXXXXXXXXXXXXX'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
photos = flickr.photos.search(tags = 'funny meme', format = 'json')



#%%
keyword = 'meme'

photos = flickr.walk(text=keyword,
                     tag_mode='all',
                     tags=keyword,
                     extras='url_c',
                     per_page=100,           # may be you can try different numbers..
                     sort='relevance')

urls = []
for i, photo in enumerate(photos):
    print (i)
    
    url = photo.get('url_c')
    urls.append(url)
    
    # get 50 urls
    if i > 1000:
        break

print (urls)

#%%

for file in urls:
    if file is not None:
        new_name = file.split('/')[-1]
        urllib.request.urlretrieve(file, new_name)
        