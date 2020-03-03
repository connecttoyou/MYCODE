import os.path
import xlwings as xw
import time
import datetime

class ToEls():
    def __init__(self):
        self._app = xw.App(visible=False, add_book=True)
        self._app.display_alerts = False
        self._app.screen_updating = False
        self._savepath='C:\\Users\\Administrator\\Desktop\\'


    def _save(self):
        today = datetime.datetime.now()
        timestr = today.strftime('%m%d') + str(today.hour) + str(today.minute) + str(today.second)#时间码，格式为“月日时分秒”
        self._wb.save(self._savepath+"支出表%s.xls" % timestr)#另存为文件，文件名后为时间码
        self._wb.close()
        self._app.quit()

    def toels(self):
        try:
            self._wb = self._app.books.open("C:\\Users\\Administrator\\Desktop\\费用支出明细表")  # 打开模板
            sheet=self._wb.sheets[0]
            col=6
            key,item=list(self._result.keys()),list(self._result.values())
            sheet.range(2, 2).value =key[0][0]
            sheet.range(3, 2).value = key[0][1]
            for value in item[0]:
                for row in range(1,9):
                    sheet.range(col,row).value=value[row-1]
                col+=1
            self._save()
        except Exception as ex :
            self._wb.close()
            self._app.quit()
            print(ex)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self,value):
        self._result=value

    def output(self):
        print (self._result)

te=ToEls()
te.result={('HJE18AE0C00001','2018中国联通湖南大客户接入新建1期工程'):[['PO-hnzy-201903261523143427','01建筑工程投资','施工费','2018/12/25','shanen',12800000,0.01
,128000],['PO-hnzy-201905130930453719','01建筑工程投资','施工费','2019/2/25','chaojie',2800000,0.01
,28000]]}
te.toels()




