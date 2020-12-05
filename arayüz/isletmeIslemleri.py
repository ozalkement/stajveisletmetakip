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
        
        yeniButton=QAction(QIcon("new.jpg"), "Yeni", self)
        yeniButton.setShortcut('Ctrl+N')
        dosya.addAction(yeniButton)
        
        Kaydet=QAction(QIcon("save.png"), "Kaydet", self)
        Kaydet.setShortcut("Ctrl+S")
        dosya.addAction(Kaydet) 
        
        duzenle=bar.addMenu("Düzenle")        
        duzenle.addAction("Kopyala")
        duzenle.addAction("Kes")
        
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
        
        
        
        self.sinif = QLabel(self)
        self.sinif.setText("Sınıfı :")
        self.sinif.setGeometry(50, 20, 100, 50)
        self.sinifText=QLineEdit(self)
        self.sinifText.move(120,35)
        self.sinifText.resize(200,20)
     
        self.ogrNo = QLabel(self)
        self.ogrNo.setText("Öğrenci No :")
        self.ogrNo.setGeometry(50, 50, 100, 50)
        self.ogrNoText=QLineEdit(self)
        self.ogrNoText.move(120,65)
        self.ogrNoText.resize(200,20)
        
        self.ad= QLabel(self)
        self.ad.setText("Ad :")
        self.ad.setGeometry(50, 80, 100, 50)
        self.adText=QLineEdit(self)
        self.adText.move(120,95)
        self.adText.resize(200,20)
        
        self.soyad = QLabel(self)
        self.soyad.setText("Soyad :")
        self.soyad.setGeometry(50, 110, 100, 50)
        self.soyadText=QLineEdit(self)
        self.soyadText.move(120,125)
        self.soyadText.resize(200,20)
        
        self.dogumTarihi = QLabel(self)
        self.dogumTarihi.setText("Doğum Tarihi :")
        self.dogumTarihi.setGeometry(50, 140, 100, 50)
        self.dogumTarihiText=QLineEdit(self)
        self.dogumTarihiText.move(120,155)
        self.dogumTarihiText.resize(200,20)
        
      
        
        
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