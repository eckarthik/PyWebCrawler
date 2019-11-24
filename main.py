import threading,os,time,argparse,warnings,time,sys
from queue import Queue
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

args = parser.parse_args()

def create_worker_threads():
    for i in range(0, args.thread_count):
        t = threading.Thread(target=work)
        #t.daemon = True
        t.start()

def add_links_to_queue():
    for link in file_to_set(project_name=args.project_name, file_name=queue_file):
        queue.put(link)
    queue.join()
    crawl()

def work():
    while True:
        url = queue.get()
        # print("Sending URL - ",url," to crawl")
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def crawl():
    links_in_queue = file_to_set(project_name=args.project_name, file_name=queue_file)
    if len(links_in_queue) > 0:
        # print("Links pending in queue - ",len(links_in_queue))
        add_links_to_queue()

if not args.base_url:
    print(parser.format_help())
else:
    domain_name = parse.urlparse(args.base_url).netloc
    queue_file = "queue.txt"
    crawled_file = "crawled.txt"
    if not args.project_name:
        args.project_name = domain_name
    if not args.thread_count:
        args.thread_count = 2

    queue = Queue()
    spider = Spider(args.project_name,domain_name,args.base_url)

    #Initialized Data
    print(Colorify.colorify("[!] BASE URL: ","YELLOW")+Colorify.colorify(" "+str(args.base_url),"GREEN"))
    print(Colorify.colorify("[!] THREAD COUNT: ", "YELLOW") + Colorify.colorify(" " + str(args.thread_count), "GREEN"))
    print(Colorify.colorify("[!] PROJECT NAME: ", "YELLOW") + Colorify.colorify(" " + str(args.project_name), "GREEN"))
    print(Colorify.colorify(" Started crawling at "+args.base_url,"ORANGE"))
    print(Colorify.colorify("------------------------------------------------------------------------------------","RED"))
    print("                                              PROGRESS                                                     ")

    time_before_start = time.time()
    create_worker_threads()
    crawl()
    time_after_completion = time.time()
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
