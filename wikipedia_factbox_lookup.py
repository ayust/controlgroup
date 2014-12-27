#!/usr/bin/env python
"""
This script takes wikipedia urls on stdin and returns the value of the factbox 'key' on stdout.

Example:

	echo 'http://en.wikipedia.org/wiki/Pluto' | ./wikipedia_factbox_lookup.py 'Discovery Date'
	February 18, 1930

The key argument is not case sensitive and you can omit spaces if you like. Below is the same as above:

	echo 'http://en.wikipedia.org/wiki/Pluto' | ./wikipedia_factbox_lookup.py discoverydate

Installation:

	pip install pyquery requests

"""
import sys
import itertools
import requests
import json
from pyquery import PyQuery as pq

def normalize_key(key):
	return unicode(key).strip().lower().replace(u' ', '').replace(u'\u00A0', u'')

key = normalize_key(sys.argv[-1])

def persist_to_file(file_name):
    def decorator(original_func):

        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache[param]

        return new_func

    return decorator

@persist_to_file('.wikipedia_factbox_cache.json')
def get_html(url):
	return requests.get(url).text

def download_and_parse(wikipedia_url):
	page = pq(url=wikipedia_url.strip(), opener=get_html)	
	key_values = {}
	for tr in page('.infobox tr'):
		tr = pq(tr)
		cells = tr('th,td')
		if len(cells) == 2:
			test_key = normalize_key(cells.eq(0).text())
			if key == test_key:
				return cells.eq(1).text().strip()

results = itertools.imap(download_and_parse, sys.stdin)
for result in results:
	if result:
		sys.stdout.write(u'{}\n'.format(result))