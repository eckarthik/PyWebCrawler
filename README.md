# Python Web Crawler

This is a web crawler tool that will help you to crawl the website you need for links.

# Features!

  - Faster
  - Ablility to specify the number of threads to use to crawl the given website
  - Ability to use proxies to bypass IP restrictions
  - Clear summary of all the urls that were crawled
  - Ability to specify delay between each HTTP Request

# Upcoming Features!

  - Search for specific text throughout the website
  - Stop and resume the crawler
  - Gather AWS Buckets,Emails,Phone Numbers etc
  - Download all images


### Dependencies

This tool uses a number of open source projects to work properly:

* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Parser to parse the HTML response of each request made to the URLs
* [Requests](https://pypi.org/project/requests/) - To make GET requests to the URLs


# Usage
Usage Instructions

```console
C:\Users\PyWebCrawler>python main.py
usage: main.py [-u BASE_URL] [-t THREAD_COUNT] [--project-name PROJECT_NAME]
               [--timeout TIMEOUT] [--delay DELAY] [--proxies PROXIES]

Fastest Web Crawler

optional arguments:
  -u BASE_URL, --url BASE_URL
                        Base URL to Crawl
  -t THREAD_COUNT, --threads THREAD_COUNT
                        Number of threads to run this crawler on
  --project-name PROJECT_NAME
                        Project Name
  --timeout TIMEOUT     HTTP request timeout
  --delay DELAY         Delay between each request
  --proxies PROXIES     Proxies to use for making HTTP requests
```
