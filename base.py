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
        self._税额 = kwargs['税额']
        self._价税合计 = kwargs['价税合计']

    def getvalue(self):
        return {'订单编号':self._订单编号,'商品名称':self._商品名称, '项目编号':self._项目编号,'项目名称':self._项目名称,'订单日期':self._订单日期,'支出类型':self._支出类型,
                '供应商':self._供应商,'数量':self._数量,'单价':self._单价,'金额':self._金额,'税额':self._税额,'价税合计':self._价税合计}


class DB():
    def __init__(self,**kwargs):
       pass

    def  setvalue(self,**kwargs):
        self.调拨单号 = kwargs['调拨单号']
        self.订单编号 = kwargs['订单编号']
        self.调出项目 = kwargs['调出项目']
        self.调入项目 = kwargs['调入项目']
        self.调拨日期 = kwargs['调拨日期']
        self.数量 = kwargs['数量']
        self.单价 = kwargs['单价']
        self.金额 = kwargs['金额']



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
# po=PO()
# po.setvalue(订单编号='123',商品名称='123',项目编号='123',项目名称='123',订单日期='123',支出类型='123',供应商='123',数量='123',单价='123',金额='123',税额='123',价税合计='123')
# dbr=DBResult()
# dbr.setXM(项目信息='123')
# dbr.setPO(po)
# print(len(dbr))

