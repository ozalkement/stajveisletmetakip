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
        self.width = 800
        self.height = 600
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
        self.sinif.setGeometry(45, 20, 100, 50) #(ayniDeger,+30,ayniDeger,ayniDeger)
        self.sinifText=QLineEdit(self)
        self.sinifText.move(120,35) #(ayniDeger,+30)
        self.sinifText.resize(200,20)
     
        self.ogrNo = QLabel(self)
        self.ogrNo.setText("Öğrenci No :")
        self.ogrNo.setGeometry(45, 50, 100, 50)
        self.ogrNoText=QLineEdit(self)
        self.ogrNoText.move(120,65)
        self.ogrNoText.resize(200,20)
        
        self.ad= QLabel(self)
        self.ad.setText("Ad :")
        self.ad.setGeometry(45, 80, 100, 50)
        self.adText=QLineEdit(self)
        self.adText.move(120,95)
        self.adText.resize(200,20)
        
        self.soyad = QLabel(self)
        self.soyad.setText("Soyad :")
        self.soyad.setGeometry(45, 110, 100, 50)
        self.soyadText=QLineEdit(self)
        self.soyadText.move(120,125)
        self.soyadText.resize(200,20)
        
        
        self.dogumTarihi = QLabel(self)
        self.dogumTarihi.setText("Doğum Tarihi :")
        self.dogumTarihi.setGeometry(45, 140, 100, 50)
          
       
        
        self.dogumTarihiText=QLineEdit(self)
        
        self.dogumTarihiText.move(120,155)
        self.dogumTarihiText.resize(200,20)
        
  
    
      
        self.telefon= QLabel(self)
        self.telefon.setText("Telefon :")
        self.telefon.setGeometry(45, 170, 100, 50)
        self.telefonText=QLineEdit(self)
        self.telefonText.move(120,185)
        self.telefonText.resize(200,20)
      
        
        
        self.veliAdSoyad= QLabel(self)
        self.veliAdSoyad.setText("Veli Ad Soyad :")
        self.veliAdSoyad.setGeometry(45, 200, 100, 50)
        self.veliAdSoyadText=QLineEdit(self)
        self.veliAdSoyadText.move(120,215)
        self.veliAdSoyadText.resize(200,20)
        
      
        self.veliTelefon= QLabel(self)
        self.veliTelefon.setText("Veli Telefonu :")
        self.veliTelefon.setGeometry(45, 230, 100, 50)
        self.veliTelefonText=QLineEdit(self)
        self.veliTelefonText.move(120,245)
        self.veliTelefonText.resize(200,20)
      
        
        self.adres= QLabel(self)
        self.adres.setText("Adres :")
        self.adres.setGeometry(45, 260, 100, 50)
        self.adresText=QLineEdit(self)
        self.adresText.move(120,275)
        self.adresText.resize(200,20)
      
        
      
        self.bolum= QLabel(self)
        self.veliTelefon.setText("Bölümü :")
        self.veliTelefon.setGeometry(45, 290, 100, 50)
        self.veliTelefonText=QLineEdit(self)
        self.veliTelefonText.move(120,305)
        self.veliTelefonText.resize(200,20)
      
        
        self.dal= QLabel(self)
        self.dal.setText("Dalı :")
        self.dal.setGeometry(45, 320, 100, 50)
        self.dalText=QLineEdit(self)
        self.dalText.move(120,335)
        self.dalText.resize(200,20)
        
      
        
      
        
      
        
        self.button=QPushButton('Ekle',self)       
        self.button.move(20,500)
        #♠self.button.clicked.connect(self.on_click)
             
        
        

        self.vbox = QVBoxLayout(self)
        self.takvim = QCalendarWidget(self)
        self.takvim.setGridVisible(True)
        self.takvim.clicked[QDate].connect(self.showDate)
        self.vbox.addWidget(self.takvim)
        
        self.tarih = self.takvim.selectedDate()
        self.dogumTarihiText.setText(self.tarih.toString())
        self.vbox.addWidget(self.dogumTarihiText)
        self.setLayout(self.vbox)
        self.takvim.setGeometry(320, 145, 420, 120)
        
        self.show()

    def showDate(self, tarih):
        self.dogumTarihiText.setText(self.tarih.toString())
def main():
    app = QApplication(sys.argv)  
   
    ex = menu()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()