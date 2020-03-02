from bs4 import BeautifulSoup
import requests
from http import cookiejar
from urllib import request
import sys
import io
import xlwings as xw
import base
import pymongo


def getPofromxls(path='')  :  # 从excel文件中获取订单信息
    po=base.PO()
    PoInfo=[]
    try:
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(path)
        sheet1 =wb.sheets[0]
        rng = sheet1.range('A1').expand('table')
        for row in range(1 ,rng.rows.count ):
            rg = rng.value[row]
            if (float(rg[19] ) >0) & (rg[39]!=''):
                po.setvalue(订单编号= rg[0],商品名称= rg[3],项目编号=rg[7],项目名称= rg[8],支出类型=rg[12],
                    供应商= rg[14],数量=int(float(rg[19])), 单价=float(rg[16]),金额=float(rg[20]),税额=float (rg[21]),价税合计=float( rg[22]),
                    订单日期=rg[39])
                yield po
        # yield PoInfo
        wb.close()
        app.quit()
    except Exception as ex:
        wb.close()
        app.quit()
        print(ex )#




class ToDB():
    def __init__(self):
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["MssInfo"]
            self._mydb=mydb["MssInfo"]
        except Exception as ex:
            print(ex)

    def save_one(self,value):
        self._mydb.insert_one(document=value)

    def save_many(self,value):
        self._mydb.insert_many(documents=value)

    def finddata(self,**kwargs):
        dbresult=base.DBResult()
        documents=self._mydb.find(kwargs)
        for document in documents:
            po = base.PO()
            document.pop('_id')
            po.setvalue(**document)
            dbresult.setPO(po)
        dbresult.setXM(项目信息=kwargs['项目编号'])
        return  dbresult


tdb=ToDB()
# for tl in getPofromxls('C:\\Users\\zx\\Downloads\\12.xls'):
#     tdb.save_one(tl.getvalue())
tdb.finddata(项目编号='HEC19AE0B00005',支出类型="01建筑工程投资")