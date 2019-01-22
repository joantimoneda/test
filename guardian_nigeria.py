
import urllib.request
from bs4 import BeautifulSoup 
from time import sleep 
from tqdm import tqdm 
from datetime import datetime, timedelta, date 
import re


# sitemap in site_url = "https://guardian.ng/sitemap.xml"

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
    hold_dict['authors'] = author.split(',')[0] # remove cities or positions
    hold_dict['date'] = ' '.join(soup.find(class_=re.compile(r'manual-age')).text.split())
    hold_dict['image_urls'] = []
    hold_dict['image_captions'] = []
    if soup.article.find_all('img'):
        hold_dict['image_urls'] = [i['src'] for i in soup.article.find_all('img') if '/plugins/' not in i['src']]
        captions = soup.find_all(class_=re.compile(r'caption'))
        hold_dict['image_captions'] = list(set([c.text.strip() for c in captions]))
    # First paragraph always hanging without tag. If all text, also caption. 
    # So take all text and remove matched caption on first par only. Hence finding captions first
    body = soup.find('article').text 
    hold_dict['paragraphs'] =  list(filter(None, body.split('\n'))) # getting paragraphs indexed by line breaks; if by 'p', first par is lost. Remove potential empty ones.
    if hold_dict['image_captions']:
        hold_dict['paragraphs'][0] = hold_dict['paragraphs'][0].replace(hold_dict['image_captions'][0], '') #remove caption match
        hold_dict['paragraphs'] = list(filter(None,  hold_dict['paragraphs'])) # Remove empty ones. Important to do this again in case all caption was first par  
    return(hold_dict)


# example url: https://guardian.ng/news/putin-warns-of-consequences-over-orthodox-split/        
# Check links 
# =============================================================================
# collect_guardianng()              
# urls = open('guardianng.txt', "r").read().splitlines() 
# for url in tqdm(urls2):   
#     html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
#     parse_guardianng(html)
#     print(url)
#     sleep(1)
# =============================================================================
    
    
    
    
    
    
    