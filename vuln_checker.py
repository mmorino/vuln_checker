# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 17:58:40 2020

@author: Masanori Morino
"""
import settings
import datetime
import requests
import xml.etree.ElementTree as ET

ns = {}
ns['xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
ns['rss'] = 'http://purl.org/rss/1.0/' 
ns['rdf'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' 
ns['dc'] = 'http://purl.org/dc/elements/1.1/' 
ns['dcterms'] = 'http://purl.org/dc/terms/' 
ns['r'] = 'http://jvn.jp/rss/mod_sec/3.0/' 
ns['marking'] = 'http://data-marking.mitre.org/Marking-1' 
ns['tlpMarking'] = 'http://data-marking.mitre.org/extensions/MarkingStructure#TLP-1' 
ns['status'] = 'http://jvndb.jvn.jp/myjvn/Status' 
ns['vuldef'] = "http://jvn.jp/vuldef/" 

url = 'https://jvndb.jvn.jp/myjvn'
    
def getVulnOverviewList(dt_target, keyword, vector, start_item, max_count_item):
    params = {}
    params['method'] = 'getVulnOverviewList'
    params['feed'] = 'hnd'
    params['datePublishedStartY'] = dt_target.year
    params['datePublishedStartM'] = dt_target.month
    params['datePublishedStartD'] = dt_target.day
    params['datePublishedEndY'] = dt_target.year
    params['datePublishedEndM'] = dt_target.month
    params['datePublishedEndD'] = dt_target.day
    params['rangeDatePublished'] = 'n'
    params['rangeDateFirstPublished'] = 'n'
    params['rangeDatePublic'] = 'n'
    params['rangeDatePublic'] = 'n'
    params['start_item'] = start_item
    params['max_count_item'] = max_count_item
    params['keyword'] = keyword
    params['vector'] = vector
    
    return requests.get(url, params=params)
                
dt_target = datetime.datetime(settings.dt_published_start_y, settings.dt_published_start_m, settings.dt_published_start_d)

vector = settings.vector

for keyword in settings.keywords:
    start_item = 1
    max_count_item = 50

    while True:
        response = getVulnOverviewList(dt_target, keyword, vector, start_item, max_count_item)

        root = ET.fromstring(response.text)    
        status = root.find('./status:Status', ns)    
        total_res = status.get('totalRes')
        if (int(total_res) == 0):
            break
        
        items = root.findall('./rss:item', ns)
        for item in items:
            title = item.find('rss:title', ns).text
            link = item.find('rss:link', ns).text
            print(title + ' ' + link)
            
        if (int(total_res) > len(items)):
            start_item += max_count_item
        else:
            break
    