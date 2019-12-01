from bs4 import BeautifulSoup
import time
from urllib import parse
from requester import Requester


class LinkFinder():

    def __init__(self, base_url, page_url, proxies, gather_titles, timeout, delay):
        self.base_url = base_url
        self.page_url = page_url
        self.delay = delay  # Delay in seconds between each HTTP Request
        self.urls = set()
        self.url_with_title = dict()
        self.gather_titles = gather_titles
        self.page_title = None
        self.requester = Requester(page_url=page_url, host=parse.urlparse(self.page_url).netloc, proxies=proxies,
                                   timeout=timeout)

    def find_urls(self):
        response = self.requester.request()
        time.sleep(self.delay)
        if isinstance(response, tuple):
            # Some error occured with the page, we did not get a response content. Returning it to the spider to handle
            return response
        else:
            bs4_object = BeautifulSoup(response, 'html.parser')
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
        to_return = dict()
        to_return["page_url"] = self.page_url
        to_return["page_title"] = self.page_title
        to_return["urls_in_page"] = self.urls
        return to_return
