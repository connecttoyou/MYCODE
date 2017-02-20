from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.request
import os
from threading import Thread
from queue import Queue
from time import time


class creatworker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            # 从队列中获取任务并扩展tuple
            url= self.queue.get()
            star(url)
            self.queue.task_done()

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            # 从队列中获取任务并扩展tuple
            url = self.queue.get()
            download_link(url)
            self.queue.task_done()

def download_link(url):
   # urllib.request.urlretrieve(link, directory)
   str = url[url.find('pictures/') + 9:]
   urllist = getlink(url, "a", "(big.jpg)")
   path = u'f:/test/' + str
   if not os.path.exists(path):
       os.makedirs(path)
   x = 0
   for url1 in urllist:
       print('现在下载的是：', '%s.jpg' % x)
       # queue.put((os.path.join(path,'%s.jpg'%x), url1))
       urllib.request.urlretrieve(url1, os.path.join(path, '%s.jpg' % x))
       x += 1



def getlink(url,tagname,reg):
    listname = []
    bsobj = BeautifulSoup( urlopen(url), "html.parser")
    for link in bsobj.findAll(tagname, href=re.compile(reg)):
        linkstr = link.attrs['href']
        linkstr = linkstr[linkstr.find('http://'):]
        if linkstr not in listname :
            listname += [linkstr]
    return listname

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)

#local = os.path.join('f:/test','Python-2.7.5.tar.bz2')
def star(url):
    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    tagname="a"
    reg="(milfbank)"
    for url in  getlink(url, tagname, reg):
        #download_link(url)
        queue.put(url)
    queue.join()


def main():
    queue= Queue()
    url = "http://www.milfbank.com/Secretary/"
    for x in range(4):
        creater=creatworker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
        creater.daemon=True
        creater.start()

    star(url)
    queue.join()


ts = time()
main()
print('Took {}'.format(time() - ts))