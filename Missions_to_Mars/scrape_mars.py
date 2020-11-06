import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    executable_path = {"executable_path": "C:\Users\stuhu\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver"}
    return Broswer("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}
    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["news_title"] = soup.find("", class_="").get_text()
    listings["news_p"] = soup.find("", class_="").get_text()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["feature_image_url"] = soup.find("", class_="").get_text()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["hemisphere_image_urls"] = soup.find("", class_="").get_text()

    url_t = "https://space-facts.com/mars/"
    tables = pd.read_html(url_t)
    df = tables[0]

    html_table = df.to_html()

    
    return html_table
    return listings