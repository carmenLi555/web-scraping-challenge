from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
  
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    #Extract news title and text 
    result = soup.find('div', class_="list_text")
    news_title = result.a.text
    news_p = result.find('div',class_="article_teaser_body").text


    # Mars Img
    images_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(images_url)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

    relative_image_path=images_soup.find('a', class_="fancybox-thumbs")
    url_base="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    url_ext = relative_image_path.attrs['href']
    featured_image_url = url_base + url_ext

    # Mars Facts

    fact_url='https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)

    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_fact.set_index("Profile",inplace=True)

    html_table = mars_fact.to_html()
    html_table.replace('\n', '')

    #Mars Hemispheres
    usgs_url='https://astrogeology.usgs.gov'
    Hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(Hem_url)
    html=browser.html
    soup= BeautifulSoup(html,'html.parser')

    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    for item in mars_item:
        hem=item.find('div',class_='description')
        title=hem.h3.text
        hem_url=hem.a['href']
        browser.visit(usgs_url+hem_url)
        html=browser.html
        soup=BeautifulSoup(html,'html.parser')
        image_src=soup.find('li').a['href']

        hem_dict={'title':title,'image_url':image_src}
        hemisphere_image_urls.append(hem_dict)
        
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":html_table,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict


    