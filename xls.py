import xlwings as xw
import os

class merge():
    def __init__(self,filepath):
        self.files=[]
        self.__file_dir=filepath
        for root, dirs, files in os.walk(self.__file_dir):
            for filespath in files:
                if (os.path.splitext(filespath)[1] == '.xls')or(os.path.splitext(filespath)[1] == '.xlsx'):
                    self.files.append(os.path.join(root, filespath))

    def run(self):
        app = xw.App(visible=True, add_book=False)
        wb = app.books.open('f:\\罗武甲供汇总.xlsx')
        for file in self.files:
            print(file)


mer=merge('F:\\集客项目\\集客项目')
mer.run()