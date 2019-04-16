#coding=utf-8
import sys
import json
import webbrowser
from data import *
from down_mark import *
from main_interface import Ui_Dialog
from add_interface import Ui_Dialog_add
from PyQt5 import QtWidgets, QtGui
from pypinyin import Style
import pypinyin

class add_window(QtWidgets.QWidget, Ui_Dialog_add):
    def __init__(self,prior):
        print(1)
        print(self)
        QtWidgets.QWidget.__init__(self)
        print(2)
        self.setupUi(self)
        print(3)
        self.prior=prior
        print(4)

    def confirm(self):
        Data.name=self.lineEdit.text()
        Data.url=self.lineEdit_2.text()
        for i in Data.urllist:
            if(Data.name==i):
                Data.urllist[i]=Data.urllist[i]+';'+Data.url
                with open('file_list.json', 'w', encoding='utf-8') as f:
                    json.dump(Data.urllist, f, ensure_ascii=False, indent=2)
                f.close()
                self.hide()               
                return
        Data.urllist.update({Data.name:Data.url})
        with open('file_list.json', 'w', encoding='utf-8') as f:
            json.dump(Data.urllist, f, ensure_ascii=False, indent=2)
        f.close()
        self.prior.adddisplay()
        self.hide()
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def cancel(self):
        self.hide()
        self.lineEdit.clear()
        self.lineEdit_2.clear()


class father_window(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(father_window, self).__init__()
        self.setupUi(self)
        for name in Data.urllist:
            self.listWidget.addItem(name)                    
        self.listWidget.doubleClicked.connect(self.open)
        self.lineEdit.textChanged.connect(self.showlist)
        self.add_app = QtWidgets.QApplication(sys.argv)
        self.add_show = add_window(self)

    def add(self):
        self.add_show.show()
                                         
    def delete(self):
        deletename=self.listWidget.currentItem().text()
        self.listWidget.takeItem(self.listWidget.currentRow())
        Data.urllist.pop(deletename)
        with open('file_list.json', 'w', encoding='utf-8') as f:
                    json.dump(Data.urllist, f, ensure_ascii=False, indent=2)
        f.close()


    def import_list(self):
        t=import1()
        if (t==1):
            information=QMessageBox.information(self,"提示","成功")
        elif (t==0):
            information=QMessageBox.information(self,"提示","没有文件导入")
            
    def open(self):
        name=self.listWidget.currentItem().text()
        urllong=Data.urllist[name]
        url=urllong.split(';')
        for thing in url:
            webbrowser.open(thing)

    def adddisplay(self):
        self.listWidget.addItem(Data.name)

    def showlist(self):
        keywd = self.lineEdit.text().strip()
        if keywd:
            self.listWidget.clear()
            # print(urllist)
            for item in Data.urllist:
                if (keywd.lower() in item.lower()) or (keywd.lower() in pypinyin.slug(item.lower(), separator='') or
                                                       (keywd.lower() in pypinyin.slug(item.lower(),
                                                                                       style=Style.FIRST_LETTER,
                                                                                       separator=''))):
                    self.listWidget.addItem(item)  # 加载搜索结果
        else:
            self.listWidget.clear()
            for item in Data.urllist:
                self.listWidget.addItem(item)  # 空字符时，加载所有列表

if __name__ == "__main__":   
    app = QtWidgets.QApplication(sys.argv)
    myshow = father_window()
    myshow.show()
    sys.exit(app.exec_())
    
