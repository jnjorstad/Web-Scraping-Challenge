#convet jupyter notebook into python script called srape_mars.py
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

def scrape():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #visit each url
    url = 'https://redplanetscience.com/'
    space_images_url = 'https://spaceimages-mars.com/'
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    mars_hemispheres_url = 'https://marshemispheres.com/'
    scrape_mars = {}
    
    #first url
    browser.visit(url)
    time.sleep(1)
    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    latest_news_title = soup.find('div', class_='content_title').get_text()
    latest_news_paragraph = soup.find('div', class_='article_teaser_body').get_text()
    
    #space images url
    browser.visit(space_images_url)
    time.sleep(1)
    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = soup.find('img', class_='headerimage fade-in').get("src")
    image_url = f"{space_images_url}{image_url}"
   
    
    #mars facts url
    browser.visit(mars_facts_url)
    time.sleep(1)
    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    table = pd.read_html(mars_facts_url)
    df= table[0]
    html_table = df.to_html()
    html_table.replace('\n', '')
    html_table
    
    #mars hemispheres url
    browser.visit(mars_hemispheres_url)
    time.sleep(1)
    #scrape page into soup
    html= browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_dict = []
    items = soup.find_all('div', class_= 'item')
    for item in items: 
        title = item.find('h3').text
        link = item.find('a', class_='itemLink')["href"]
        hemisphereslink = mars_hemispheres_url + link
        browser.visit(hemisphereslink)
        hemispherehtml = browser.html
        soup2 = bs(hemispherehtml, 'html.parser')
        img = soup2.find('img', class_= 'wide-image')["src"]
        imgurl = mars_hemispheres_url + img
        hemisphere_image_dict.append({"Title": title, "img_url": imgurl})
    hemisphere_image_dict

    #store data in a dictionary 
    scrape_mars["latest_news_title"] = latest_news_title
    scrape_mars["latest_news_paragraph"] = latest_news_paragraph
    scrape_mars["image_url"] = image_url
    scrape_mars["html_table"] = html_table
    scrape_mars["hemisphere_image_dict"] = hemisphere_image_dict

    #close browser after scraping
    browser.quit()

    #return results
    return scrape_mars
