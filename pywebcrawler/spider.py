from pywebcrawler.utilities import *
from pywebcrawler.link_finder import LinkFinder
import sys
from pywebcrawler.colorify import Colorify


class Spider:
    """Spider Class"""

    project_name = ''
    queue_file = ''
    crawled_file = ''
    urls_with_titles_file = ''
    domain_name = ''
    base_url = ''
    proxies = None
    timeout = None
    delay = None
    gather_titles = None
    search_text = None
    queue = set()
    crawled = set()
    connection_errors = set()
    unknown_errors = set()
    timeout_errors = set()
    too_many_redirects_errors = set()
    file_links = set()

    def __init__(self, project_name, domain_name, base_url, timeout, delay, gather_titles, search_text, proxies=None):
        Spider.project_name = project_name
        Spider.domain_name = domain_name
        Spider.base_url = base_url
        Spider.queue_file = "queue.txt"
        Spider.crawled_file = "crawled.txt"
        Spider.urls_with_titles_file = "urls_with_titles.csv"
        Spider.proxies = proxies
        Spider.timeout = timeout
        Spider.delay = delay
        Spider.gather_titles = gather_titles
        Spider.search_text = search_text
        self.startup()
        self.crawl_page("First Page", page_url=base_url)

    @staticmethod
    def startup():  # Creates required files on startup
        create_directory(Spider.project_name)
        create_files(Spider.project_name, Spider.queue_file, data=Spider.base_url)
        create_files(Spider.project_name, Spider.crawled_file, data='')
        if Spider.gather_titles:
            create_csv_file(Spider.project_name, Spider.urls_with_titles_file,
                            header_row=["URL", "TITLE"])  # File to store urls with their titles
        Spider.queue = file_to_set(project_name=Spider.project_name, file_name=Spider.queue_file)
        Spider.crawled = file_to_set(project_name=Spider.project_name, file_name=Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if not page_url in Spider.crawled:
            if not Spider.queue == 1:
                sys.stdout.write(Colorify.colorify(
                    "                               In Queue - {0}         Crawled - {1}                         \r".format(
                        len(Spider.queue), len(Spider.crawled)), "GREEN"))
                sys.stdout.flush()
            links_finder = LinkFinder(base_url=Spider.base_url, page_url=page_url, proxies=Spider.proxies,
                                      gather_titles=Spider.gather_titles, search_text=Spider.search_text, timeout=Spider.timeout, delay=Spider.delay)
            links_from_link_finder = links_finder.get_urls()
            if isinstance(links_from_link_finder,
                          tuple):  # We got some errors with one of the link, let's handle and categorize them
                if links_from_link_finder[1] == "TooManyRedirects":
                    Spider.too_many_redirects_errors.add(links_from_link_finder[0])
                    Spider.update_queue_crawled_files(links_from_link_finder[0])
                elif links_from_link_finder[1] == "ConnectionError":
                    Spider.connection_errors.add(links_from_link_finder[0])
                    Spider.update_queue_crawled_files(links_from_link_finder[0])
                elif links_from_link_finder[1] == "Timeout":
                    Spider.timeout_errors.add(links_from_link_finder[0])
                    Spider.update_queue_crawled_files(links_from_link_finder[0])
                elif links_from_link_finder[1] == "UnknownError":
                    Spider.unknown_errors.add(links_from_link_finder[0])
                    Spider.update_queue_crawled_files(links_from_link_finder[0])
                elif links_from_link_finder[1] == "File":
                    Spider.file_links.add(links_from_link_finder[0])
                    Spider.update_queue_crawled_files(links_from_link_finder[0])

            else:
                if Spider.gather_titles:
                    # Save the url and its title
                    append_to_csv(Spider.project_name, Spider.urls_with_titles_file,
                                  data=[links_from_link_finder["page_url"], links_from_link_finder["page_title"]])
                # We got a bunch of links from the link finder
                Spider.add_links_to_queue(links_from_link_finder["urls_in_page"])
                Spider.update_queue_crawled_files(page_url)

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            if (link not in Spider.queue) and (link not in Spider.crawled):
                Spider.queue.add(link)

    @staticmethod
    def update_queue_crawled_files(url):
        """Removes from queue and updates the crawled"""

        Spider.queue.remove(url)
        Spider.crawled.add(url)
        Spider.save_data_to_files()

    @staticmethod
    def save_data_to_files():
        set_to_file(project_name=Spider.project_name, data=Spider.queue, file_name=Spider.queue_file)
        set_to_file(project_name=Spider.project_name, data=Spider.crawled, file_name=Spider.crawled_file)