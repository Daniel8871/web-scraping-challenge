from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# First URL
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    # Grabbing titles and text from redplanetscience.com
    news_title = soup.find('div',class_='content_title').get_text()
    news_body = soup.find('div', class_='article_teaser_body').get_text()

# 2nd URL - Scraping featured image
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    time.sleep(2)
    html_img = browser.html
    soup = BeautifulSoup(html_img,'html.parser')
    img_feature = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = url2+img_feature

# 3rd URL - Grabbing table
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    time.sleep(2)
    mars_table = tables[0]
    mars_table.columns = ['Description', 'Mars','Earth']
    mars_table.set_index('Description',inplace=True)
    mars_table = mars_table.to_html()
    
# 4th URL - Grabbing 4 hemisphere images
    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    time.sleep(2)
    html_hemi = browser.html
    soup = BeautifulSoup(html_hemi,'html.parser')

    img_items = soup.find_all('div',class_='description')

    # Gather the links to each hemispheres site from the main page
    urls = []
    for img in img_items:
        link = img.find('a',class_="itemLink product-item")
        urls.append(link['href'])

    hemisphere_img_urls = []

    # Loop through each of the sites to grab the full size images and titles
    for url in urls:
        browser.visit(url4+url)
        html_astro = browser.html
        soup = BeautifulSoup(html_astro,'html.parser')

        name_hemi = soup.find_all('h2', class_='title')
        tif = soup.find_all('a', string='Sample')

        hemisphere_img_urls.append({'title':name_hemi[0].text,
                            'img_url':url4+tif[0]['href']})    

    
    mars_list={'news_title':news_title,'news_body':news_body,
        'featured_image_url': featured_image_url, 'mars_table':mars_table,
        'hemisphere_img_urls':hemisphere_img_urls }
    browser.quit()

    return mars_list




