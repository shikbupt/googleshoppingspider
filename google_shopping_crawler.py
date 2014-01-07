from download_pics import MyThread
from download_pics import download_pics
from analyse_web_pages import WebPageAnalysis
from Queue import Queue
from random import randint
from time import sleep
import threading


def main():
    search_class = ['shoes']
    max_download_threads = 10
    root = 'z:\\'
    threads = []
    queue = Queue()
    for item in search_class:
        url = 'http://www.google.co.uk/search?q=%s&tbm=shop&ei=HAGYUujUEIfvkQWPTw&ved=0CAMQyBAoAQ&pshpl=1&pshplp=2&num=10' % item
        t = threading.Thread(target=WebPageAnalysis(url, queue))
        threads.append(t)
        for i in xrange(1,max_download_threads):
            t = MyThread(download_pics, (root+item+'\\', queue), 'download_pics')
            threads.append(t)
    threads[0].start()
    for i in threads[1:]:
        i.setDaemon(True)
        i.start()
    
    threads[0].join()

    while not queue.empty():
        pass
    sleep(5)

if __name__ == '__main__':
    main()