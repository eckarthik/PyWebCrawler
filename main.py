import argparse
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from urllib import parse

from colorify import Colorify
from spider import Spider
from utilities import *

warnings.filterwarnings('ignore')

# Process the command line arguments
parser = argparse.ArgumentParser(description="Fastest Web Crawler", add_help=False)
parser.add_argument("-u", "--url", help="Base URL to Crawl", dest='base_url')
parser.add_argument("-t", "--threads", help="Number of threads to run this crawler on", dest='thread_count', type=int)
parser.add_argument("--project-name", help="Project Name", dest='project_name')
parser.add_argument("--timeout", help="HTTP request timeout", dest='timeout', type=int)
parser.add_argument("--delay", help="Delay between each request", dest='delay', type=int)
parser.add_argument("--proxies", help="Proxies to use for making HTTP requests", dest='proxies')
parser.add_argument("--depth", help="Number of levels to crawl", dest="depth", type=int)
parser.add_argument("--gather-titles", help="Creates a CSV file with page urls and their respective titles",
                    dest="gather_titles", type=bool)
parser.add_argument("--search-text", help="Search for the text throughout the website",
                    dest="search_text", type=str)

args = parser.parse_args()


def work(url):
    Spider.crawl_page("", url)
    queue.remove(url)


def fill_queue():
    for link in file_to_set(project_name=project_name, file_name=queue_file):
        queue.add(link)


def run(links):
    executor = ThreadPoolExecutor(max_workers=thread_count)
    futures = [executor.submit(work, link) for link in links]  # Not bothering about results of futures for time being.
    executor.shutdown(wait=True)

    # Tool name
print(Colorify.colorify(Colorify.colorify("""
    ____       _       __     __    ______                    __         
   / __ \__  _| |     / /__  / /_  / ____/________ __      __/ /__  _____
  / /_/ / / / / | /| / / _ \/ __ \/ /   / ___/ __ `/ | /| / / / _ \/ ___/
 / ____/ /_/ /| |/ |/ /  __/ /_/ / /___/ /  / /_/ /| |/ |/ / /  __/ /    
/_/    \__, / |__/|__/\___/_.___/\____/_/   \__,_/ |__/|__/_/\___/_/     
      /____/

    ""","BOLD"),"GREEN"))
if not args.base_url:
    print(parser.format_help())
else:
    domain_name = parse.urlparse(args.base_url).netloc
    queue_file = "queue.txt"
    crawled_file = "crawled.txt"
    project_name = args.project_name or domain_name
    thread_count = args.thread_count or 4
    delay = args.delay or 0
    timeout = args.timeout or 5
    depth = args.depth or -1
    gather_titles = args.gather_titles or False
    search_text = args.search_text or None

    # Initialized Data
    print(Colorify.colorify("[!] BASE URL: ", "YELLOW") + Colorify.colorify(" " + str(args.base_url), "GREEN"))
    print(Colorify.colorify("[!] THREAD COUNT: ", "YELLOW") + Colorify.colorify(" " + str(thread_count), "GREEN"))
    print(Colorify.colorify("[!] PROJECT NAME: ", "YELLOW") + Colorify.colorify(" " + str(project_name), "GREEN"))
    print(Colorify.colorify(" Started crawling at " + args.base_url + "\n", "ORANGE"))
    print(Colorify.colorify("------------------------------------------------------------------------------------",
                            "RED"))

    # Check if project already exists
    if check_project_directory_exists(project_name):
        if len(file_to_set(project_name, queue_file)) == 0:
            print(Colorify.colorify(
                "[!] You already have a project directory with some data. Do you want to override? (yes/no)", "RED"))
            choice = str(input())
            if choice.lower() == "yes":
                # Deleting existing project directory
                delete_project(project_name)
                print(Colorify.colorify(
                    "[!] Deleted existing project directory",
                    "GREEN"))
                pass
            elif choice.lower() == "no":
                print(Colorify.colorify(
                    "[!] Please delete the existing directory or pass --project-name parameter with a new name",
                    "RED"))
                sys.exit(0)
            else:
                sys.exit(0)
        elif len(file_to_set(project_name, queue_file)) >= 1:
            print(Colorify.colorify(
                "[!] There are some links already in queue. Do you want to resume from there? (yes/no)", "RED"))
            choice = str(input())
            if choice.lower() == "yes":
                # Resume the scan
                pass
            elif choice.lower() == "no":
                print(Colorify.colorify(
                    "[!] Please delete the existing directory or pass --project-name paramter with a different name for the project",
                    "RED"))
                sys.exit(0)
            else:
                sys.exit(0)

    # Handle the proxies if passed
    proxies = []
    if args.proxies:
        print(Colorify.colorify("[*] Checking the proxies......", "GREEN"))
        # Proxies were passed in the CLI arguments
        for proxy in args.proxies.split(","):
            if check_proxy(proxy):
                proxies.append(proxy)
        if len(proxies) == 0:
            print(Colorify.colorify(
                "[!] None of the passed proxies were alive. Proceeding to crawl without using any proxies",
                "GREEN"))
            spider = Spider(project_name, domain_name,
                            args.base_url, timeout, delay, gather_titles, search_text)
        else:
            print(Colorify.colorify(
                "[!] " + str(len(proxies)) + " were alive. Proceeding to crawl ny using these proxies",
                "GREEN"))
            spider = Spider(project_name, domain_name,
                            args.base_url, timeout, delay, gather_titles, search_text, proxies=proxies)
    else:
        spider = Spider(project_name, domain_name,
                        args.base_url, timeout, delay, gather_titles, search_text)

    queue = set()  # Internal queue to store the links
    print("                                              PROGRESS                                                     ")
    time_before_start = time.time()  # Note down the time at the start of crawling

    """ Starting to crawl the links """
    fill_queue()  # Fill the queue with the links obtained from base url
    depth2 = 0
    if depth == -1:  # Crawl until the user stops
        while True:
            if len(queue) > 0:
                run(queue)
                fill_queue()
            else:
                break
            depth2 += 1
            print(" \n                                     Completed crawling", depth2, "level ")
    else:
        while depth > 0:
            run(queue)
            fill_queue()
            depth -= 1
            depth2 += 1
            print(" \n                                     Completed crawling", depth2, "level ")

    """Crawled all the links"""
    time_after_completion = time.time()  # Note down the time at the end of crawling

    print(Colorify.colorify("-------------------------------------------------------------------------------------",
                            "RED"))
    print("                                              SUMMARY                                                     ")
    print("Time Taken - ", float(time_after_completion - time_before_start), " seconds")
    print("Speed - ", int(len(spider.crawled) / (time_after_completion - time_before_start)), " requests/second")
    print("Files - ", len(spider.file_links))
    print("Unknown Errors - ", len(spider.unknown_errors))
    print("Timeout Errors - ", len(spider.timeout_errors))
    print("Connection Errors - ", len(spider.connection_errors))
    print("TooManyRedirect Errors - ", len(spider.too_many_redirects_errors))
