# Python Web Crawler [![Build Status](https://travis-ci.org/eckarthik/PyWebCrawler.svg?branch=master)](https://travis-ci.org/eckarthik/PyWebCrawler)

A web crawler written in Python to crawl a given website.

# Features!

  - Faster
  - Ablility to specify the number of threads to use to crawl the given website
  - Ability to use proxies to bypass IP restrictions
  - Clear summary of all the urls that were crawled. View the crawled.txt file to see the complete list of all the links crawled
  - Ability to specify delay between each HTTP Request
  - Stop and resume crawler whenever you need
  - Gather all the urls with their titles to a csv, incase if you are planning to create a search engine
  - Search for specific text throughout the website
  - Clear statistics about how many links ended up as Files,Timeout Errors,Connecrion Errors
  - Crawl until you need. You can specify upto what level the crawler should crawl.
  - Random browser user agents will be used while crawling.

# Upcoming Features!

  - Gather AWS Buckets,Emails,Phone Numbers etc
  - Download all images

### Dependencies

This tool uses a number of open source projects to work properly:

* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Parser to parse the HTML response of each request made.
* [Requests](https://pypi.org/project/requests/) - To make GET requests to the URLs.

### Usage
If you like to see the list of supported features, simply run
![Usage Demo](https://i.ibb.co/8zVss64/Running-Main-Py.png)

###### Specifying only to crawl for 3 levels
![Depth Crawl](https://i.ibb.co/TTF8g2X/Running-Main-Py.png>)
###### Search for specific text throughout the website
![Text Search](https://i.ibb.co/q9trhVp/Running-Main-Py.png)
###### Gather all the links along with their titles to a CSV file. A CSV file with the links and their titles will be created after the crawl completes
![Gather Titles](https://i.ibb.co/6sDD2cC/Running-Main-Py.png)
###### Use proxies to crawl the site. 
![Use Proxies](https://i.ibb.co/51SwP7m/Running-Main-Py.png)
