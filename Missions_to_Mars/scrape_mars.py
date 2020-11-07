import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs


def init_browser():
    executable_path = {"executable_path": "/Users/stuhu/.wdm/drivers/chromedriver/win32/86.0.4240.22/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}
    
# NASA Mars News
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_='list_text')
    title = results.find('div', class_='content_title')
    news_title = title.a.text
    news = results.find('div', class_='article_teaser_body')
    news_p = news.text

# JPL Mars Space Images -Featured Image
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_2_og = "https://www.jpl.nasa.gov"
    browser.visit(url_2)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find('img', class_='main_image')
    image_src = image['src']
    feature_image_url = url_2_og + image_src

# Mars Hemispheres
    url_4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_4_og = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    hemisphere_list = [
        "Cerberus Hemisphere", "Schiaparelli Hemisphere",
        "Syrtis Major Hemisphere", "Valles Marineris Hemisphere"
        ]
    for hemisphere in hemisphere_list:
        browser.visit(url_4)
        browser.links.find_by_partial_text(f'{hemisphere} Enhanced').click()
        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")
        results = soup.find('img', class_='wide-image')
        link = results['src']
        full_link = url_4_og + link
        temp_dict = {
            "title": f"{hemisphere}",
            "img_url": full_link
            }
        hemisphere_image_urls.append(temp_dict)

    browser.quit()


    listings["news_title"] = news_title
    listings["news_p"] = news_p
    listings["feature_image_url"] = feature_image_url
    #listings["html_table"] = 
    listings["title1"] = hemisphere_image_urls[0]["title"]
    listings["img_url1"] = hemisphere_image_urls[0]["img_url"]
    #listings["img_url2"] = 
    #listings["title3"] = 
    #listings["img_url3"] = 
    #listings["title4"] = 
    #listings["img_url4"] = 
    print(listings)

    browser.quit()

    return listings

scrape()
