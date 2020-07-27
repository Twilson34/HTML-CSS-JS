from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import time
import re


def scrape_all():
    """Call all other functions"""
    # Initiate headless driver for deployment
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "main_image": featured_image(browser),
        "hemispheres": scrape_hemi(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
        }
    browser.quit()
    return data


def mars_news(browser):
    """Scrape Mars NEws"""
    #Website Location
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    #puteverything in a beautiful soup
    html = browser.html
    soup=bs(html, 'html.parser')
    try:
        slide = soup.select_one("ul.item_list li.slide")
        #captured all of the titles 
        news_title=slide.find('div', class_="content_title").get_text() 
        #capturing the paragraph below title
        news_paragraph=slide.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph
    

def featured_image(browser):
    """Collect Main Image"""
    # Define URL & Visit
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    #Scraping image page
    soup=bs(browser.html, 'html.parser')
    test=soup.body.find('img', class_="main_image")
    image_address=test['src']
    main_image=f'https://www.jpl.nasa.gov{image_address}'
    return main_image

def twitter_weather(browser):
    "Mars Weather"
    
    #Define URL
    twit_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twit_url)
    while True:
        if not browser.is_element_not_present_by_tag('article'):
            break
    twit_html = browser.html
    soup = bs(twit_html, 'html.parser')
    tweets = soup.find('article')
    
    for tweet in tweets:
        spans = tweet.find_all("span")
        mars_weather = spans[4].get_text()
        #Replacing all paragraph breaks
        # weather = weather.replace('\n', " ")
        return mars_weather

def mars_facts():
    """Mars Facts"""
    url="https://space-facts.com/mars/)"
    mars_table=pd.read_html(url)
    ctable=mars_table[0]
    final_table=ctable.rename(columns={0:'Description',1: "value"})
    return final_table.to_html(header=True, index=True)

def scrape_hemi(browser):
    """Collect Hemispheres"""
    hems=['Cerberus Hemisphere Enhanced','Schiaparelli Hemisphere Enhanced','Syrtis Major Hemisphere Enhanced','Valles Marineris Hemisphere Enhanced']
    hems_url=[]

    for info in hems: 
        home_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(home_url)
        browser.is_element_present_by_text(info, wait_time=1)
        more_info_elem = browser.find_link_by_partial_text(info)
        more_info_elem.click()
        full_image_elem = browser.find_by_id('wide-image-toggle')
        full_image_elem.click()
        soup=bs(browser.html, 'html.parser')
        photo1=soup.body.find('img', class_='wide-image')
        photo_src=photo1['src']
        photo_url1=f"https://astrogeology.usgs.gov{photo_src}"
        hems_url.append(photo_url1)  
        return(photo_url1)

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": hems_url[0]},
    {"title": "Cerberus Hemisphere", "img_url":hems_url[1]},
    {"title": "Schiaparelli Hemisphere", "img_url": hems_url[2]},
    {"title": "Syrtis Major Hemisphere", "img_url": hems_url[3]},]
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())