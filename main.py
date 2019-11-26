import argparse,warnings,time,sys
from concurrent.futures import ThreadPoolExecutor
from utilities import *
from spider import Spider
from urllib import parse
from colorify import Colorify
warnings.filterwarnings('ignore')

#Process the command line arguments
parser = argparse.ArgumentParser(description="Fastest Web Crawler",add_help=False)
parser.add_argument("-u","--url",help="Base URL to Crawl",dest='base_url')
parser.add_argument("-t","--threads",help="Number of threads to run this crawler on",dest='thread_count',type=int)
parser.add_argument("--project-name",help="Project Name",dest='project_name')
parser.add_argument("--timeout",help="HTTP request timeout",dest='timeout',type=int)
parser.add_argument("--delay",help="Delay between each request",dest='delay',type=int)
parser.add_argument("--proxies",help="Proxies to use for making HTTP requests",dest='proxies')
parser.add_argument("--depth",help="Number of levels to crawl",dest="depth",type=int)

args = parser.parse_args()

def work(url):
    Spider.crawl_page("",url)
    queue.remove(url)

def fill_queue():
    for link in file_to_set(project_name=project_name, file_name=queue_file):
        queue.add(link)

def run(links):
    executor = ThreadPoolExecutor(max_workers=thread_count)
    futures = [executor.submit(work,link) for link in links] #Not bothering about the results of futures for the time being.
    executor.shutdown(wait=True)

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


    # Initialized Data
    print(Colorify.colorify("[!] BASE URL: ", "YELLOW") + Colorify.colorify(" " + str(args.base_url), "GREEN"))
    print(Colorify.colorify("[!] THREAD COUNT: ", "YELLOW") + Colorify.colorify(" " + str(thread_count),"GREEN"))
    print(Colorify.colorify("[!] PROJECT NAME: ", "YELLOW") + Colorify.colorify(" " + str(project_name),"GREEN"))

    #Handle the proxies if passed
    proxies = []
    if args.proxies:
        print(Colorify.colorify("[*] Checking the proxies......","GREEN"))
        #Proxies were passed in the CLI arguments
        for proxy in args.proxies.split(","):
            if check_proxy(proxy):
                proxies.append(proxy)
    if len(proxies)==0:
        print(Colorify.colorify("[!] None of the passed proxies were alive. Proceeding to crawl without using any proxies", "GREEN"))
        spider = Spider(project_name, domain_name,
                        args.base_url,timeout,delay)  # Instantiate the Spider. Will crawl the Base URL and store all the URLs present in first page into queue_file
    else:
        print(Colorify.colorify("[!] "+str(len(proxies))+" were alive. Proceeding to crawl ny using these proxies", "GREEN"))
        spider = Spider(project_name, domain_name,
                        args.base_url,timeout,delay,proxies=proxies)  # Instantiate the Spider. Will crawl the Base URL and store all the URLs present in first page into queue_file

    queue = set() #Internal queue to store the links

    print(Colorify.colorify(" Started crawling at "+args.base_url,"ORANGE"))
    print(Colorify.colorify("------------------------------------------------------------------------------------","RED"))
    print("                                              PROGRESS                                                     ")

    time_before_start = time.time() #Note down the time at the start of crawling

    ### Starting to crawl the links ###
    fill_queue() #Fill the queue with the links obatained from base url
    print("Initial Queue Length = ", len(queue))
    if depth==-1:# Crawl until the user stops
        while True:
            if len(queue)>0:
                run(queue)
                fill_queue()
            else:
                break

            print("Queue Length = ",len(queue))
    else:
        while depth>0:
            run(queue)
            fill_queue()
            depth-=1
            print("Current remaining depth = ", depth)


    ### End of crawling all links ###

    time_after_completion = time.time() #Note down the time at the end of crawling

    print(Colorify.colorify("-------------------------------------------------------------------------------------","RED"))
    print("                                              SUMMARY                                                     ")
    print("Time Taken - ",float(time_after_completion-time_before_start)," seconds")
    print("Speed - ",int(len(spider.crawled)/(time_after_completion-time_before_start))," requests/second")
    print("Unknown Errors - ",len(spider.unknown_errors))
    print("Timeout Errors - ",len(spider.timeout_errors))
    print("Connection Errors - ",len(spider.connection_errors))
    print("TooManyRedirect Errors - ",len(spider.too_many_redirects_errors))
    print("Files ",len(spider.file_links))
    sys.exit(0)
