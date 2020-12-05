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
        self.setWindowIcon(QIcon("icon.png"))
        
        
       
        self.initUI()
    def initUI(self):
        
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        
        self.etiket = QLabel(self)
        self.etiket.setPixmap(QPixmap("stajIsletme.png"))
        
        self.etiket.move(70,100)

        self.etiket.setGeometry(0,0,640,400)
        
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
        
        
        
        
       
        
        
              
        self.show()

def main():
    app = QApplication(sys.argv)
    

   
    pencere = menu()
    
    pencere.show()
    
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()