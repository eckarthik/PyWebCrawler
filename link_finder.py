from bs4 import BeautifulSoup
import requests,time
from urllib import parse
from requester import Requester
class LinkFinder():

    def __init__(self,base_url,page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.requester = Requester(page_url=page_url,host=parse.urlparse(self.page_url).netloc)

    def find_links(self):
        response = self.requester.request()
        if isinstance(response,tuple):
            #Some error occured with the page, we did not get a response content
            #Returning it to the spider to handle
            print("Tuple - ",response)
            return response
        else:
            bs4_object = BeautifulSoup(response,'html.parser')
            all_anchor_tags = bs4_object.find_all('a')
            for anchor_tag in all_anchor_tags:
                href = anchor_tag.get('href')
                if href != "":
                    url = parse.urljoin(self.base_url,anchor_tag.get('href')) #If the href value contains a relative link, create the full link by using the base url. But if href value conatins a full link, then don't do anything. This is automatically handled by urljoin method
                    if parse.urlparse(url).netloc != parse.urlparse(self.base_url).netloc: #Don't go out of the given site
                        continue
                    self.links.add(url)
            return self.links

    def get_links(self):
        self.find_links()
        return self.links
