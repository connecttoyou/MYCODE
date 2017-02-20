from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.request
import os

def getlink(url,tagname,reg):
    listname = []
    bsobj = BeautifulSoup( urlopen(url), "html.parser")
    for link in bsobj.findAll(tagname, href=re.compile(reg)):
        linkstr = link.attrs['href']
        #linkstr = linkstr[linkstr.find('http://'):]
        if linkstr not in listname :
            linkstr=re.sub('/','',linkstr)
            if ((linkstr=='')|(linkstr=='#')|('http' in linkstr)):
                continue
            else :
                listname += [linkstr]
    return listname

url="http://www.milfbank.com/"
tagname="a"
reg="((?!^(http:).)*)"
print(getlink(url,tagname,reg))