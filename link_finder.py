from bs4 import BeautifulSoup
import time
from urllib import parse
from requester import Requester
class LinkFinder():

    def __init__(self,base_url,page_url,proxies,timeout,delay):
        self.base_url = base_url
        self.page_url = page_url
        self.delay = delay #Delay in seconds between each HTTP Request
        self.links = set()
        self.requester = Requester(page_url=page_url,host=parse.urlparse(self.page_url).netloc,proxies=proxies,timeout=timeout)

    def find_links(self):
        response = self.requester.request()
        time.sleep(self.delay)
        if isinstance(response,tuple):
            #Some error occured with the page, we did not get a response content. Returning it to the spider to handle
            return response
        else:
            bs4_object = BeautifulSoup(response,'html.parser')
            all_anchor_tags = bs4_object.find_all('a')
            for anchor_tag in all_anchor_tags:
                href = anchor_tag.get('href')
                if href != "" and href is not None:
                    url = parse.urljoin(self.base_url,anchor_tag.get('href')) #If the href value contains a relative link, create the full link by using the base url. But if href value conatins a full link, then don't do anything. This is automatically handled by urljoin method
                    if not parse.urlparse(self.base_url).netloc in parse.urlparse(url).netloc: #Don't go out of the given site
                        continue
                    if "#" in href:
                        continue
                    self.links.add(url)
            return self.links

    def get_links(self):
        self.find_links()
        return self.links
