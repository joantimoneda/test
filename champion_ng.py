
# champion news ng 

%reset -f
#cd ./Desktop
import urllib.request
from bs4 import BeautifulSoup 
from time import sleep 
from tqdm import tqdm 
from datetime import datetime, timedelta, date 
import re


# sitemap in: "http://www.championnews.com.ng/sitemap_index.xml"

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

def xml_champion_gen(num):
    return f'http://www.championnews.com.ng/post-sitemap{num}.xml'
# No years or months, just a sequence
    
def collect_champion():
    num = range(1, 2)
    sitemaps = [xml_champion_gen(n) for n in num]
    for sm in tqdm(sitemaps): 
        links = read_sitemap(sm)
        with open('champion.txt', 'a') as f:
            for url in links:
                f.write(url + '\n')
              

def parse_champion(html):
    hold_dict = {}    
    soup = BeautifulSoup(html, 'lxml')
    hold_dict['title'] = soup.find('h1', {'class': 'entry-title'}).text
    hold_dict['date'] = soup.find('time', {'class':re.compile(r'entry-date')}).text
    body = soup.article.find_all('p')
    pars = [par.text for par in body]  
    if soup.find(class_=re.compile(r'caption')):
        hold_dict['image_captions'] = soup.find(class_=re.compile(r'caption')).text 
        pars = [par.split('\n') for par in pars if par != hold_dict['image_captions']]
        pars = sum(pars,[]) #unlist one
        #if they exist, image captions are first paragraph, hence odd placement here
    else:
         hold_dict['image_captions'] = []
        # image caption removed if it happens to be first paragraph --rare but needs to be done    
    if pars[0].split(' ')[0].isupper(): # best I could think of is consistency around caps for author names
        hold_dict['author'] = pars[0].split(',')[0] #sometimes city is in there
        hold_dict['paragraphs'] = [par.split('\n') for par in pars if hold_dict['author'] not in par]
    else:
        hold_dict['author'] = []
        hold_dict['paragraphs'] = [par.split('\n') for par in pars]
    if not hold_dict['paragraphs']:
        hold_dict['paragraphs'] = pars
            # have to dump everything at some point, this is already a condition fest
    hold_dict['image_urls'] = []
    if soup.article.find('img', {'class':'entry-thumb'}):
        hold_dict['image_urls'] = soup.article.find('img', {'class':'entry-thumb'})['src']
    return(hold_dict)
         
#collect_guardianng()              
urls = open('champion.txt', "r").read().splitlines() 
urls = urls[37:len(urls)] #first url with actual content is 37

url

url = urls[44]
url
html = urllib.request.urlopen(url).read()
parse_champion(html)

urls2 = urls[25:125]
for url in tqdm(urls2):   
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
    parse_champion(html)
    print(url)
    sleep(0.5)

url = "http://www.championnews.com.ng/inec-speaks-possibility-postponing-elections/"






pars = [par.text for par in body]
pars2 = [par.split('\n') for par in pars if par != hold_dict['image_captions']]
pars2[0][0]


url = "https://www.nan.ng/news/apc-pdp-in-peaceful-rallies/"












