import xlwings as xw
import os


# 用于汇总项目设计物资


class mergexls():
    def __init__(self, filepath=''):
        # self.filepath=filepath
        self.file = []
        self.result = {}
        self.info=os.listdir(filepath)[0]
        for root, dirs, files in os.walk(filepath):
            # for dir in dirs:
            #     print( os.path.join(root, dir));#.decode('gbk').encode('utf-8'));

            for file in files:
                file_path = os.path.join(root, file)  # .decode('gbk').encode('utf-8'));
                if ((file_path.endswith("xlsx")) or (file_path.endswith("xls"))):
                    self.file.insert(0, file_path)
        # for file in os.walk(filepath):
        #     for each_list in file[2]:
        #         file_path = file[0] + "/" + each_list
        #         # os.walk()函数返回三个参数：路径，子文件夹，路径下的文件，利用字符串拼接file[0]和file[2]得到文件的路径
        #         if ((file_path.endswith("xlsx"))or(file_path.endswith("xls"))):
        #              self.file.insert(0, file_path)
        # app=xw.App(visible=True,add_book=False)
        # app.display_alerts=False
        # app.screen_updating=False
        # self.wb=app.books.open(self.filepath)

    def getdate(self):
        savepath = "E:\\工作\2019\\集客项目审计\\2018年项目\\罗武\\罗武甲供汇总.xlsx"
        item = []
        try:
            app = xw.App(visible=True, add_book=False)
            app.display_alerts = False
            app.screen_updating = False
            wb1 = app.books.open(savepath)
            sht1 = wb1.sheets["Sheet1"]
            sht1.range("a1").value, sht1.range("b1").value = "母项目名称", "子项目名称"
            def summ(sht: xw.sheets,value:list,srange):
                # rg=xw.Range()
                # rg.address
              try:
                rng = sht.range(srange)
                # rnge=sht.range('e7:e36')
                for rg in rng:
                    if ((rg.value == None)):  # or(sht.range('g'+rg.address.split("$")[2]).value==None)):#or(sht.range('b' + rg.address.split("$")[2]).value=='甲供材料费(合计)')):
                        continue
                    # elif(sht.range('b' + rg.address.split("$")[2]).value=='甲供材料费(合计)'):
                    #     continue
                    elif(rg.value >0):
                        value.append([(sht.range('b' + rg.address.split("$")[2]).value), rg.value])
              except Exception as e:
                  print (e)
            j, k = 2, 1
            for path in self.file:
                print(path)
                wb = app.books.open(path)
                # info=()
                value = []
                sht = wb.sheets[0]
                info=sht.range('b2').value
                print(info,' ',k)
                k+=1
                if (wb.sheets[7].name=="(表四)(需安装的设备)"):
                    sht = wb.sheets["(表四)(需安装的设备)"]
                    summ(sht,value,'e7:e45')
                    sht = wb.sheets["(表四)(甲供材料)"]
                    summ(sht,value,'e7:e33')
                else:
                    sht = wb.sheets["(表四)甲(主材调整为设备表)"]
                    summ(sht, value,'f8:f65')
                wb.save()
                wb.close()
                i='a'
                sht1.range(i + str(j)).value, sht1.range('b' + str(j)).value = self.info, info
                for val in value:
                    if (val[0] not in item):
                        item.append(val[0])
                        if (len(item) < 25):
                            sht1.range(chr(ord(i) + 1 + len(item)) + str(1)).value = val[0]
                            sht1.range(chr(ord(i) + 1 + len(item)) + str(j)).value = val[1]
                        else:
                            sht1.range('a' + chr(ord(i) + len(item) - 25) + str(1)).value = val[0]
                            sht1.range('a' + chr(ord(i) + len(item) - 25) + str(j)).value = val[1]
                    else:
                        if (item.index(val[0]) < 24):
                            sht1.range(chr(ord(i) + 2 + item.index(val[0])) + str(j)).value = val[1]
                        else:
                            sht1.range('a' + chr(ord(i) + item.index(val[0]) - 24) + str(j)).value = val[1]
                print(info+' '+"saved")
                j += 1
                wb1.save()
            wb1.close
            app.quit()
            app.kill()
            print("完成！")
        except Exception as e:
            wb.close()
            wb1.close()
            app.quit()
            app.kill()
            print(e)




mg = mergexls("E:\\工作\\2019\\集客项目审计\\2018年项目\\罗武\\集客项目\\集客项目")
mg.getdate()

# filepath="E:/工作/2019/财务相关/转资/集客/18年/"
# savepath="E:/工作/2019/财务相关/转资/集客/汇总.xlsx"
# app = xw.App(visible=True, add_book=False)
# app.display_alerts = False
# app.screen_updating = False
# wb1 = app.books.open(savepath)
# sht1 = wb1.sheets["Sheet1"]
# j=1
# try:
#     for root, dirs, files in os.walk(filepath):
#         for file in files:
#         #file_path = os.path.join(root, file)  # .decode('gbk').encode('utf-8'));
#             if ((file.endswith("xlsx")) or (file.endswith("xls"))):
#                 print(os.path.join(root, file) ,'  ',j)
#                 sht1.range('a'+str(j)).value,sht1.range('b'+str(j)).value=root[root.index('18年')+4:],file
#                 j+=1
# except Exception as e:
#     print(e)
# wb1.save()
# wb1.close()
# app.quit()
# app.kill()#mg.savedate()