import xlwings as xw
from base import *
import os
from getxls import *

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
        print(ex )

def DBtoPO():#爬取调拨单信息，并将点播但转换成订单后存入数据库
    cookie_str = "SESSION=69eef33e-23ad-484b-8f31-96ee6442a52d; NTKF_T2D_CLIENTID=guestD39A76D9-9CB2-D451-1271-A1F19DB6A748; LtpaToken=tQX78YHEEn1YBvIwIQdNNzNwQ8Sv9jiPOt7XKCqQnqRRmyaXBVcIDLbW1vn4E0FC4uQoBKnEtv96016BbU7hKthdAYTYzvYEL4e1cFDNZhixr1BYAZNUBekIU+i3Gbcy7AVAVCNyKsKLAEc6u+qOkFjrMNeJunE+ydkG5D72rfe2BuH7R2z5nVoZ8fZZnFgzH+WhiyqGTxrVS07YoVi5cPDfoq+DxGQr1VJSrAxZ6mGEiv9FoqkPPixaBEeR4PBJLNi2zZPcOvvyU7q6GF9FAB3vObByRF4MjR8KnTxlo+4=; aiportalut=QnNqNN4T/mSsOslHWJspY7N1a+8UBfEPzMXKyByE0xA=; nTalk_CACHE_DATA={uid:bl_1000_ISME9754_guestD39A76D9-9CB2-D4,tid:1583219785513166}"
    url = 'http://www.eshop.unicom.local:8080/eshop/newprojectChange/queryChangeOrder.do?current=16&shopCode=hnyiy&type=in&page.currentPage=1&pageChangeFlag=1'
    db = DB()
    tdb=ToDB()
    gdb=GetDB()
    gdb.cookie(cookie_str)
    # DBlink_list=gdb.url(url)
    for link in gdb.url(url):
        db.setvalue(**gdb.getDBinfo(link))
        l,n=db.ToPo(tdb)
        tdb.save_one("MssInfo",l.getvalue())
        tdb.save_one("MssInfo",n.getvalue())
    tdb.close()
    print("调拨单转成订单完成！")

def savetoMDB(path='C:\\Users\\zx\\Downloads\\34.xls'):#从excel获取订单信息后存入数据库
    tdb=ToDB()
    for tl in getPofromxls(path):
         tdb.save_one("MssInfo",tl.getvalue())
    tdb.close()
    print("订单存入数据库完成！")

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
        print(ex )





#DBtoPO()

tdb=ToDB()



toecl=ToEls()
toecl.result=tdb.findpo(订单编号='PO-hnzy-20190722155634513',支出类型="01建筑工程投资")
toecl.toels()

tdb.close()
