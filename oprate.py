import xlwings as xw
from base import PO,DBResult,GetDB,DB
import pymongo
import os

def getPofromxls(path='')  :  # 从excel文件中获取订单信息
    po=PO()
    try:
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(path)
        sheet1 =wb.sheets[0]
        rng = sheet1.range('A1').expand('table')
        for row in range(1 ,rng.rows.count ):
            rg = rng.value[row]
            if (float(rg[19] ) >0) & (rg[39]!=''):
                po.setvalue(订单编号= rg[0],商品名称= rg[3],项目编号=rg[7],项目名称= rg[8],支出类型=rg[12],
                    供应商= rg[14],数量=int(float(rg[19])), 单价=float(rg[16]),金额=float(rg[20]),调拨单号='',价税合计=float( rg[22]),
                    订单日期=rg[39])
                yield po
        # yield PoInfo
        wb.close()
        app.quit()
    except Exception as ex:
        wb.close()
        app.quit()
        print(ex )#

def getPrjfromxls(path='')  :  # 从excel文件中获取项目名称和编号
    try:
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(path)
        sheet1 =wb.sheets[0]
        rng = sheet1.range('A1').expand('table')
        for row in range(0 ,rng.rows.count ):
            rg = rng.value[row]
            yield {"项目编号":rg[0],"项目名称":rg[1]}
        wb.close()
        app.quit()
    except Exception as ex:
        wb.close()
        app.quit()
        print(ex )#




class ToDB():
    def __init__(self):
        try:
            self._myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            self._con=self._myclient["MssInfo"]

        except Exception as ex:
            print(ex)


    def save_one(self,con,value):
        mydb=self._con[con]
        mydb.insert_one(document=value)

    def save_many(self,con,value):
        mydb = self._con[con]
        mydb.insert_many(documents=value)

    def _find(self,con,**kwargs):
        if con=='prj':
            mydb = self._con[con]
            return mydb.find_one(kwargs)
        elif con=="MssInfo":
            mydb = self._con[con]
            return mydb.find(kwargs)
        else :
            raise Exception("数据库错误")

    def  findpo(self,**kwargs):
        documents=self._find("MssInfo",**kwargs)
        dbresult = DBResult()
        for document in documents:
            po = PO()
            document.pop('_id')
            po.setvalue(**document)
            dbresult.setPO(po)

    def findpri(self,**kwargs):
        return self._find("prj", **kwargs).pop("_id")



    def close(self):
        self._myclient.close()


cookie_str ='SESSION=86403084-95f7-426c-832e-383500b95a00; NTKF_T2D_CLIENTID=guestD39A76D9-9CB2-D451-1271-A1F19DB6A748; LtpaToken=tQX78YHEEn1YBvIwIQdNNzNwQ8Sv9jiPOt7XKCqQnqRRmyaXBVcIDCDDuq+PNAww4uQoBKnEtv96016BbU7hKthdAYTYzvYEL4e1cFDNZhixr1BYAZNUBekIU+i3Gbcy7AVAVCNyKsKLAEc6u+qOkFjrMNeJunE+ydkG5D72rfe2BuH7R2z5nVoZ8fZZnFgzH+WhiyqGTxrVS07YoVi5cPDfoq+DxGQr1VJSrAxZ6mGEiv9FoqkPPixaBEeR4PBJLNi2zZPcOvvyU7q6GF9FAB3vObByRF4MjR8KnTxlo+4=; aiportalut=o7Ou2ts6UgfrpXSWs2dezdGYpuY3YNRObVkszGXn0h0='
url='http://www.eshop.unicom.local:8080/eshop/newprojectChange/queryChangeOrder.do?current=16&shopCode=hnyiy&type=in&page.currentPage=1&pageChangeFlag=1'


tdb=ToDB()
db=DB()
gdb=GetDB()
gdb.cookie(cookie_str)
DBlink_list=gdb.url(url)
for link in gdb.url(url):
    db.setvalue(**gdb.getDBinfo(link))
# for tl in getPrjfromxls('C:\\Users\\zx\\Downloads\\56.xls'):
#     tdb.save_one(tl)

# #     print('result')
# result=tdb.findpo(项目编号='HEC19AE0B00005',支出类型="01建筑工程投资")
tdb.findpri(项目名称='2019年中国联通湖南益阳宽带接入新建7期工程')
tdb.close()
print(os.getcwd())