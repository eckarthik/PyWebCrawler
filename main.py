import threading,os,time
from queue import Queue
from utilities import *
from spider import Spider

project_name = "resblog"
base_url = "http://localhost/resblog"
domain_name = "localhost"
max_threads = 1
queue_file = "queue.txt"
crawled_file = "crawled.txt"

queue = Queue()
spider = Spider(project_name,domain_name,base_url)


def create_worker_threads():
    for i in range(0,max_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def add_links_to_queue():
    for link in file_to_set(project_name=project_name,file_name=queue_file):
        queue.put(link)
    queue.join()
    crawl()

def work():
    while True:
        url = queue.get()
        # print("Sending URL - ",url," to crawl")
        spider.crawl_page(threading.current_thread().name,url)
        queue.task_done()

def crawl():
    links_in_queue = file_to_set(project_name=project_name,file_name=queue_file)
    if len(links_in_queue) > 0:
        # print("Links pending in queue - ",len(links_in_queue))
        add_links_to_queue()

create_worker_threads()
crawl()

print("Summarizing Data - ")
print("Unknown Errors - ",spider.unknown_errors)
print("Timeout Errors - ",spider.timeout_errors)
print("Connection Errors - ",spider.connection_errors)
print("TooManyRedirect Errors - ",spider.too_many_redirects_errors)
print("Files ",str(spider.file_links))
