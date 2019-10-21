from bs4 import BeautifulSoup as bs
from splinter import Browser
import datetime as dt
import pandas as pd


def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    mars_info = {}
    browser = init_browser()

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')

    news_list = nasa_soup.find('ul', class_='item_list')
    news_item = news_list.find('li', class_='slide')
    news_title = news_item.find('div', class_='content_title').text
    news_paragraph = news_item.find('div', class_='article_teaser_body').text

    mars_info["news_title"] = news_title
    mars_info["news_paragraph"] = news_paragraph

    # ### JPL Mars Space Images - Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    full_image_button = jpl_soup.find(class_='button fancybox')
    href = full_image_button['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{href}'

    mars_info["featured_image_url"] = featured_image_url

    # ### Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    mars_twitter = browser.html
    twitter_soup = bs(mars_twitter, 'html.parser')

    mars_tweets = twitter_soup.find('ol', class_='stream-items')
    mars_weather = mars_tweets.find('p', class_="tweet-text").text

    mars_info["mars_weather"] = mars_weather

    # ### Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_facts_html = browser.html
    mars_facts_soup = bs(mars_facts_html, 'html.parser')

    mars_profile = mars_facts_soup.find(
        'table', class_='tablepress tablepress-id-p-mars')
    column1 = mars_profile.find_all('td', class_='column-1')
    column2 = mars_profile.find_all('td', class_='column-2')

    dimensions = []
    values = []

    for row in column1:
        dimension = row.text.strip()
        dimensions.append(dimension)

    for row in column2:
        value = row.text.strip()
        values.append(value)

    mars_facts = pd.DataFrame({
        "Description": dimensions,
        "Value": values
    })

    mars_facts = mars_facts.set_index("Description")
    print(mars_facts)
    mars_facts_html = mars_facts.to_html('mars_facts.html')

    mars_info["mars_facts"] = mars_facts_html

    # Mars Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    hemisphere_images = []

    for i in range(4):

        images = browser.find_by_tag('h3')
        images[i].click()
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, 'html.parser')

        partial_url = hemi_soup.find("img", class_="wide-image")["src"]
        image_title = hemi_soup.find("h2", class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+partial_url

        image_dict = {"title": image_title, "image_url": image_url}
        hemisphere_images.append(image_dict)

        print(image_title)
        print(image_url)

        browser.back()
    mars_info["hemisphere_images"] = hemisphere_images

    browser.quit()

    return mars_info
