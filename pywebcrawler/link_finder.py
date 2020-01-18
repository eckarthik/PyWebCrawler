from bs4 import BeautifulSoup
import time
from urllib import parse
from pywebcrawler.requester import Requester


class LinkFinder():

    error_with_link_flag = False
    error_with_link_detail = None

    def __init__(self, base_url, page_url, proxies, gather_titles, search_text, timeout, delay):
        self.base_url = base_url
        self.page_url = page_url
        self.delay = delay  # Delay in seconds between each HTTP Request
        self.urls = set()
        self.url_with_title = dict()
        self.gather_titles = gather_titles
        self.page_title = None
        self.search_text = search_text
        self.requester = Requester(page_url=page_url, host=parse.urlparse(self.page_url).netloc, proxies=proxies,
                                   timeout=timeout)

    def find_urls(self):
        response = self.requester.request()
        time.sleep(self.delay)
        if isinstance(response, tuple):
            # Some error occured with the page, we did not get a response content. Returning it to the spider to handle
            LinkFinder.error_with_link_flag = True
            LinkFinder.error_with_link_detail = response
        else:
            bs4_object = BeautifulSoup(response, 'html.parser')
            if self.search_text is not None:
                if self.search_text.lower() in bs4_object.find('body').text.lower():
                    print("Given search text was found in - ", self.page_url)
            self.page_title = bs4_object.find("title").text
            all_anchor_tags = bs4_object.find_all('a')
            for anchor_tag in all_anchor_tags:
                href = anchor_tag.get('href')
                if href != "" and href is not None:
                    """
                    If the href value contains a relative link, create the full link by using the base url. 
                    But if href value conatins a full link, then don't do anything. 
                    This is automatically handled by urljoin method
                    """
                    url = parse.urljoin(self.base_url, anchor_tag.get(
                        'href'))
                    if not parse.urlparse(self.base_url).netloc in parse.urlparse(
                            url).netloc:  # Don't go out of the given site
                        continue
                    if "#" in href:
                        continue
                    self.urls.add(url)

    def get_urls(self):
        self.find_urls()
        if LinkFinder.error_with_link_flag:
            LinkFinder.error_with_link_flag = False
            return LinkFinder.error_with_link_detail
        else:
            to_return = dict()
            to_return["page_url"] = self.page_url
            to_return["page_title"] = self.page_title
            to_return["urls_in_page"] = self.urls
            return to_return
