import urllib
import os
import threading
from Queue import Queue

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args

    def getResult(self):
        return self.res

    def run(self):
        self.res=apply(self.func, self.args)

def download_pics(path, queue):
    while not queue.empty():
        temp = queue.get()
        tile = temp[0].keys()[0]
        new_dir = os.path.join(path, tile)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        for url in temp:
            key = url.keys()[0]
            pic_name = ''.join((new_dir, '\\', key, '.jpg'))
            urllib.urlretrieve(url[key], pic_name)
        queue.task_done()

def main():
    q = Queue()
    temp = [{u'11624868652670913275': u'http://t0.gstatic.com/shopping?q=tbn:ANd9GcQsCxZGmLoMPfbU5tX1wUI-MJj0r3PfMatKeQoLfdx3T-3TVfsZ2_SIjo37VlKWYdZAG3pWF88p&usqp=CAY'},
{u'11232974292547268062': u'http://t3.gstatic.com/shopping?q=tbn:ANd9GcR56CL9GlfT-kip_NTI2afQqgfbqD1q1_Yi5nzzg9KkOu4SRYM03a9XlCkKM_hUbPbfZYVmivYo&usqp=CAY'}]
    temp1 = [{u'9934237550465132614': u'http://t1.gstatic.com/shopping?q=tbn:ANd9GcRRwHNHdCPYSAT960yCbvMtT0HDmDmJAFD5YYF7CZpqDRoV91gXRwp5_ebJgxwVonv8niKDW1aK&usqp=CAY'},
{u'8546833712098233773': u'http://t0.gstatic.com/shopping?q=tbn:ANd9GcTwPAVj6YAXwZuuhYUuF_isJRoxBXPGjyqOSXd9QRPAgx-E1F3ohVA39oOBTTcWD6r9_A-i1UPf&usqp=CAY'}]
    q.put(temp)
    q.put(temp1)
    download_pics('z:\\', q)
if __name__ == '__main__':
    main()