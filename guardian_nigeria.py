
# guardian.ng 
# 8th most widely read in Nigeria based on this very scientific source: https://answersafrica.com/top-10-nigerian-newspapers-most-read-online.html
%cd './Desktop'
%reset -f
import urllib.request
from bs4 import BeautifulSoup 
from time import sleep 
from tqdm import tqdm 
from datetime import datetime, timedelta, date 
import re


# sitemap in: 

site_url = "https://guardian.ng/sitemap.xml"

def read_sitemap(site_url, compressed=False):   
    req = urllib.request.Request(site_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    if compressed:
        gunzip_response = gzip.GzipFile(fileobj=response)
        content = gunzip_response.read()
        c_d = content.decode('utf-8')
    else:
        c_d = response.read()    
    re_soup = BeautifulSoup(c_d, 'lxml')
    urls = [loc.string for loc in re_soup.find_all('loc')]
    sleep(1)
    return urls

def xml_guardianng_gen(year, month):
    if not type(month) is str:
        month = str(month)
        if len(month) < 2:
            month = '0' + month
    return f'https://guardian.ng/sitemap-pt-post-{year}-{month}.xml'

    
def collect_guardianng():
    years = range(2018, 2019)
    months = range(10, 13)
    sitemaps = [xml_guardianng_gen(year, month) for year in years for month in months]
    for sm in tqdm(sitemaps): 
        links = read_sitemap(sm)
        with open('guardianng.txt', 'a') as f:
            for url in links:
                f.write(url + '\n')
              

def parse_guardianng(html):
    hold_dict = {}    
    soup = BeautifulSoup(html, 'lxml')
    hold_dict['title'] = soup.find(class_=re.compile(r'after-category')).text.replace("\xa0", "") 
    author = soup.find(class_=re.compile(r'author')).text.strip().replace("By ", "")
    if ',' in author:  # split() won't give you error
        hold_dict['authors'] = author[0:(str.find(author, ','))] # keeping only first author if there are multiple. Doing this because city often included
    else:
        hold_dict['authors'] = author 
    date = soup.find(class_=re.compile(r'manual-age')).text.strip()
    .join(soup.find...strip()) #replace with this, keep time
    hold_dict['date'] = date[0:(str.find(date, "\xa0"))] # Date
    article_body = soup.find('article')
    body = [paragraph.text for paragraph in article_body.find_all('p', recursive=False)]
    hold_dict['paragraphs'] = [par.split("\n\xa0\n") for par in body if par is not ''] # getting paragraphs indexed by line breaks too
    if soup.article.find_all('img'):
        names = [i['src'] for i in soup.article.find_all('img')]
        hold_dict['image_urls'] = [n for n in names if '1x1.trans' not in n]
        captions = soup.find_all(class_=re.compile(r'caption'))
        hold_dict['image_captions'] = list(set([c.text.strip() for c in captions]))
    else: 
        hold_dict['image_urls'] = []
        hold_dict['image_captions'] = []
    return(hold_dict)
         
#collect_guardianng()              
urls = open('guardianng.txt', "r").read().splitlines() 
#html = urllib.request.urlopen(urls[0]).read()
urls2 = urls[0:10]
url = urls2[0]
for url in tqdm(urls2):   
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
    parse_guardianng(html)
    print(url)
    sleep(0.5)
      
bod = soup.find('div', {'class':'single-article-content'})
text = bod.article.text
cap = bod.find('div', class_='wp-caption alignnone').text
text.replace(cap, '')

types = [type(ii) for ii in bod]

## LOOK INTO DATETIME OBJECTS


# Still catching some crap at the beginning of the text and sometimes not capturing first paragraph
# because it's poorly tagged. Fix this somehow. 
    
    
    
    
    
    