import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs


def init_browser():
    executable_path = {"executable_path": "/Users/stuhu/.wdm/drivers/chromedriver/win32/89.0.4389.23/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    
# NASA Mars News
    # visit website
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    time.sleep(1)
    # scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    # find the data
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
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find('img', class_='main_image')
    image_src = image['src']
    image_find = soup.find('header', id='page_header')
    image_title = image_find.h1.text.strip()
    image_date = soup.find('span', class_='release_date').text
    image_date = image_date.replace("| ", "")
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
        time.sleep(1)
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

# Mars Facts
    url_3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url_3)
    df = tables[0]
    df.columns = ["Description", "Mars"]
    df.set_index("Description", inplace = True)
    df.rename_axis(None, inplace = True)
    html_table = df.to_html()
    html_table = html_table.replace("\n", "")

    # store data in a dictionary
    listings = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_image_url": feature_image_url,
        "image_title": image_title,
        "image_date": image_date,
        "html_table": html_table,
        "title1": hemisphere_image_urls[0]["title"],
        "img_url1": hemisphere_image_urls[0]["img_url"],
        "title2": hemisphere_image_urls[1]["title"],
        "img_url2": hemisphere_image_urls[1]["img_url"],
        "title3": hemisphere_image_urls[2]["title"],
        "img_url3": hemisphere_image_urls[2]["img_url"],
        "title4": hemisphere_image_urls[3]["title"],
        "img_url4": hemisphere_image_urls[3]["img_url"]
    }

    # quit the browser after scraping
    browser.quit()

    # return results
    return listings