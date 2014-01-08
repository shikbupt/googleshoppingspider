from download_pics import MyThread
from download_pics import download_pics
from analyse_web_pages import WebPageAnalysis
from Queue import Queue
from random import randint
from time import sleep, ctime
import threading
import os


def main():
    print 'start:', ctime()
    search_class = ['shirt']
    max_download_threads = 20
    analysis_pages = 2 # each page has 100 pics
    root = 'z:\\'
    threads = []
    queue = Queue()
    for item in search_class:
        root_path = ''.join((root, item))
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        for i in range(0,analysis_pages):
            url = 'http://www.google.co.uk/search?q=%s&tbm=shop&ei=HAGYUujUEIfvkQWPTw&ved=0CAMQyBAoAQ&pshpl=1&pshplp=2&num=100&start=%s' \
                    % (item, i*100)
            print url
            t = threading.Thread(target=WebPageAnalysis(url, queue))
            threads.append(t)
        for i in range(0,max_download_threads):
            t = MyThread(download_pics, (root_path+'\\', queue), 'download_pics')
            threads.append(t)

    for i in range(0,analysis_pages): 
        threads[i].start()
    for i in threads[analysis_pages:]:
        i.setDaemon(True)
        i.start()
    
    for i in range(0,analysis_pages): 
        threads[i].join()

    while not queue.empty():
        pass
    sleep(20)
    print 'end:', ctime()

if __name__ == '__main__':
    main()