from bs4 import BeautifulSoup
import urllib2
import re
from Queue import Queue

class WebPageAnalysis(object):
    """Analyse web page to get the url of pics for download"""

    def __init__(self, url, queue):
        super(WebPageAnalysis, self).__init__()
        self.download(url)
        self.pics_page = {}
        self.queue = queue

    def download(self, url):
        #different 'user-agent' has different return web
        heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7',
        'Accept-Language':'zh-cn,zh;q=0.5',
        'Connection':'keep-alive',
        'Keep-Alive':'115',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}    
        req = urllib2.Request(url, headers=heads)    
        self.soup = BeautifulSoup(urllib2.urlopen(req).read())

    def get_pics_pages(self):
        """get the url of the web pages including pics """

        tag = self.soup.find_all('a', href=re.compile("/shopping/product/.*"))
        for href in tag:
            url = href['href']
            pic_id = url[len("/shopping/product/"):url.index('?')]
            if not pic_id in self.pics_page:
                self.pics_page[pic_id] = url

    def get_pic_url(self):
        """get the url of pic for download"""

        for key in self.pics_page:
            self.download('http://www.google.co.uk/'+self.pics_page[key])
            tag = self.soup.find_all('img', src=True, limit=2)
            pics_url_list = [dict(zip([key], [tag[1]['src']]))]
            tag = self.soup.find_all('a', class_="vs-url")
            for href in tag:
                url = href['href']
                pic_id = url[len("/shopping/product/"):url.index('?')]
                pic_url = href.img['src']
                pics_url_list.append(dict(zip([pic_id], [pic_url])))
            self.queue.put_nowait(pics_url_list)

    def run(self):
        self.get_pics_pages()
        self.get_pic_url()

    def __call__(self):
        self.run()
                
def main():
    url = 'http://www.google.co.uk/search?q=shoes&tbm=shop&ei=HAGYUujUEIfvkQWPTw&ved=0CAMQyBAoAQ&pshpl=1&pshplp=2&num=10'
    q = Queue()
    web_annlysis = WebPageAnalysis(url, q)
    web_annlysis.run()
    logfile = open('z:\\log2.txt', 'w')
    while not q.empty():
        temp = q.get()
        for url in temp:
            print >> logfile, url
        print >> logfile, '*****************************************'
    
if __name__ == '__main__':
    main()