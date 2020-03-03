from bs4 import BeautifulSoup
import requests


class PO():
    def __init__(self):
        pass
    def  setvalue(self,**kwargs):
        self._订单编号 = kwargs['订单编号']
        self._商品名称 = kwargs['商品名称']
        self._项目编号 = kwargs['项目编号']
        self._项目名称 = kwargs['项目名称']
        self._订单日期 = kwargs['订单日期']
        self._支出类型 = kwargs['支出类型']
        self._供应商 = kwargs['供应商']
        self._数量 = kwargs['数量']
        self._单价 = kwargs['单价']
        self._金额 = kwargs['金额']
        self._调拨单号 = kwargs['调拨单号']
        self._价税合计 = kwargs['价税合计']

    def getvalue(self):
        return {'订单编号':self._订单编号,'商品名称':self._商品名称, '项目编号':self._项目编号,'项目名称':self._项目名称,'订单日期':self._订单日期,'支出类型':self._支出类型,
                '供应商':self._供应商,'数量':self._数量,'单价':self._单价,'金额':self._金额,'调拨单号':self._调拨单号,'价税合计':self._价税合计}


class DB():
    def __init__(self,**kwargs):
       pass

    def  setvalue(self,**kwargs):
        self.调拨单号 = kwargs['调拨单号']
        self.订单号 = kwargs['订单号']
        self.调出项目 = kwargs['调出项目']
        self.调入项目 = kwargs['调入项目']
        self.调拨日期 = kwargs['调拨日期']
        self.数量 = kwargs['数量']
        self.单价 = kwargs['单价']
        self.金额 = kwargs['金额']
        self.支出类型=kwargs['支出类型']
        self._供应商 = kwargs['供应商']
        self._价税合计 = kwargs['价税合计']
        self._商品名称 = kwargs['商品名称']


class DBResult():
    def __init__(self):
        self._订单信息=[]

    def setXM(self,**kwargs):
        self._项目信息=kwargs['项目信息']
    def setPO(self,value):
        self._订单信息.append(value)

    def getvalue(self) -> dict :
        return {self._项目信息:self._订单信息}

    def __len__(self):
        return len(self._订单信息)

class GetDB():
    def __init__(self):
        self._cookie={}
        self._DBInfo=[]
        self._headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    def cookie(self,cookies):
        for line in cookies.split(';'):# 把cookie字符串处理成字典，以便接下来使用
            key, value = line.split('=', 1)
            self._cookie[key] = value


    #从给定的链接获取所有需要爬取的链接
    def url(self,url):
        DBlink_list=[]
        resp = requests.get(url, headers=self._headers, cookies=self._cookie)
        soup = BeautifulSoup(resp.text, 'lxml')
        span = soup.find_all('b')
        page = int(span[len(span) - 1].contents[0])#获得总页数
        # page=1
        for page in range(1,page+1):
            newurl=url.replace('currentPage=1','currentPage=%s'%page)#第page页的链接
            try:
                resp = requests.get(newurl, headers=self._headers, cookies=self._cookie)
                soup = BeautifulSoup(resp.text, 'lxml')
                for idx, tr in enumerate(soup.find_all('tr')):
                    if idx >= 3:
                        tds = tr.find_all('td')
                        # print(tds)
                        if ((len(tds) >= 6)):# & (len(tds[6]) == 3)):
                            tls = tds[0].contents[1]
                            yield {
                                    '调拨单号': tls.contents[0],  # 获得调拨单编号
                                    'link':tls.attrs['href'], # 获取订单调拨单链接
                                    '调出项目': tds[1].contents[0].replace("\r\n",'').replace("\t",'').replace(' ',''),
                                    '调入项目': tds[2].contents[0].replace("\r\n",'').replace("\t",'').replace(' ',''),
                                    '调拨日期':tds[5].contents[0].replace("\r\n",'').replace("\t",'').replace(' ','')

                                }
                        else:
                            continue
                    # return DBlink_list
            except:
                with Exception as ex:
                    print(ex)

    def getDBinfo(self,info):
        try:
                resp = requests.get(info['link'], headers=self._headers, cookies=self._cookie)
                soup = BeautifulSoup(resp.text, 'lxml')
                trs=soup.find_all("tr")
                info.update({"订单号":trs[1].text[trs[1].text.find('PO'):trs[1].text.find('调')].replace("\n",'').replace("\r",'').replace(" ",'')})
                ss=trs[10].contents[7].text.replace(" ", '').replace("\r\n\t", '').replace("￥", '')
                info.update({"金额": float(ss)})
                ss=trs[10].contents[3].text.replace(" ",'').replace("\r\n\t",'')
                info.update({'数量':int(ss)})
                ss = trs[10].contents[5].text.replace(" ", '').replace("\r\n\t", '').replace("￥", '')
                info.update({'单价':float(ss)})
                ss=trs[7].contents[1].contents[3].text
                info.update({'支出类型':ss})
                info.pop('link')
                return info
        except:
            with Exception as ex:
                print(ex)


