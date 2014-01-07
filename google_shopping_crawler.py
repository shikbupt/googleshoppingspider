from download_pics import MyThread
from download_pics import download_pics
from analyse_web_pages import WebPageAnalysis
from Queue import Queue
from random import randint
from time import sleep
import threading

def get_queue(queue, logfile): 
    while True:
        temp = queue.get()
        for url in temp:
            print >> logfile, url
        print >> logfile, '*****************************************'
        queue.task_done()

def main():
    search_class = ['shoes']
    threads = []
    queue = Queue()
    for item in search_class:
        url = 'http://www.google.co.uk/search?q=%s&tbm=shop&ei=HAGYUujUEIfvkQWPTw&ved=0CAMQyBAoAQ&pshpl=1&pshplp=2&num=10' % item
        #t = MyThread(WebPageAnalysis, (url, queue), 'WebPageAnalysis')
        t = threading.Thread(target=WebPageAnalysis(url, queue))
        threads.append(t)
    threads[0].start()

    logfile = open('z:\\log4.txt', 'w')
    t = MyThread(get_queue, (queue, logfile), 'get_queue')
    t.setDaemon(True)
    threads.append(t)
    threads[1].start()
    
    threads[0].join()
    #threads[1].join()

    while not queue.empty():
        pass
    sleep(5)

    '''logfile = open('z:\\log3.txt', 'w')
    while not queue.empty():
        temp = queue.get()
        for url in temp:
            print >> logfile, url
        print >> logfile, '*****************************************'
    '''

if __name__ == '__main__':
    main()