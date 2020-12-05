# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 12:51:21 2020

@author: Şermin
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class menu(QMainWindow):
    def __init__(self, parent=None):
        super(menu, self).__init__(parent)
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 400
        self.initUI()
    def initUI(self):
        
        self.setGeometry(self.left,self.top,self.width,self.height)
        layout = QHBoxLayout()
        bar=self.menuBar()
        dosya=bar.addMenu("Dosya")
        
        ogrenciIslemleri=QAction(QIcon("new.jpg"), "Öğrenci İşlemleri", self)
        
        dosya.addAction(ogrenciIslemleri)
        
        isletmeIslemleri=QAction(QIcon("save.png"), "İşletme İşlemleri", self)
        
        dosya.addAction(isletmeIslemleri) 
        
        
        aramaMenu=bar.addMenu("Arama")
        aramaMenu.addAction("Bul")
        
        araclarMenu=bar.addMenu("Araçlar")
        araclarMenu.addAction("Seçenekler")
        
        yardımMenu=bar.addMenu("Yardım")
        yardımMenu.addAction("Hakkımızda")
        
        cikisButton=QAction(QIcon("exit24.png"), "Çıkış", self)
        cikisButton.setShortcut('Ctrl+Q')
        cikisButton.setStatusTip('Uygulamadan Çık')
        cikisButton.triggered.connect(self.close)
        dosya.addAction(cikisButton)
        


        self.setLayout(layout)
        self.setWindowTitle("Staj ve İşletme Takip-Öğrenci İşlemleri")
        
        
        
        
      
        
        
        self.button=QPushButton('Tamam',self)
        
        self.button.move(20,300)
        #♠self.button.clicked.connect(self.on_click)
     
        
     
        
               
               
        self.show()

def main():
    app = QApplication(sys.argv)
   


    
    ex = menu()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()