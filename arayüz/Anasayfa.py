# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:51:47 2020

@author: Şermin
"""


from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QIcon
class Tab(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MESLEKİ VE TEKNİK EĞİTİM KURUMLARI STAJ TAKİP YAZILIMI")
        self.setWindowIcon(QIcon("icon.png"))
        #self.setStyleSheet('background-color:grey')
        vbox = QVBoxLayout()
        tabWidget = QTabWidget()
        #buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        #buttonbox.accepted.connect(self.accept)
        #buttonbox.rejected.connect(self.reject)
        tabWidget.setFont(QtGui.QFont("Sanserif", 10))
        tabWidget.addTab(TabOgrenci(), "Öğrenci Ekle/Çıkar")
        tabWidget.addTab(TabIsletme(), "İşletme Ekle/Çıkar")
        tabWidget.addTab(TabRapor(), "Rapor Al")
        tabWidget.addTab(TabGrafik(), "Grafik Oluştur")
        vbox.addWidget(tabWidget)
        #vbox.addWidget(buttonbox)
        self.setLayout(vbox)
        self.setGeometry(100, 100, 500, 500)
class TabOgrenci(QWidget):
    def __init__(self):
        super().__init__()
        gBoxOgrenci= QGroupBox("Öğrenci Bilgileri")
        
        ad = QLabel()
        ad.setText("Ad")
        adText=QLineEdit()
        
        soyad = QLabel()
        soyad.setText("Soyad")
        soyadText=QLineEdit()
        
        ogrNo = QLabel()
        ogrNo.setText("Öğrenci No")
        ogrNoText=QLineEdit()
        
        sinifSube = QLabel()
        sinifSube.setText("Sınıf-Şube")
        sinifSubeText=QLineEdit()
        
        telefon = QLabel()
        telefon.setText("Telefon")
        telefonText=QLineEdit()
        
        alan = QLabel()
        alan.setText("Alan")
        alanText=QLineEdit()
                
        dal = QLabel()
        dal.setText("Dal")
        dalText=QLineEdit()
        
        
        egitimYili = QLabel()
        egitimYili.setText("Eğitim Yılı")
        egitimYiliText=QLineEdit()
        
        
        isletme = QLabel()
        isletme.setText("İşletme")
        isletmeText=QLineEdit()
        


        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(ad)
        vbox1.addWidget(adText)
        vbox1.addWidget(soyad)
        vbox1.addWidget(soyadText)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)  
        vbox1.addWidget(ogrNo)
        vbox1.addWidget(ogrNoText)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)
        vbox1.addWidget(telefon)
        vbox1.addWidget(telefonText)
        vbox1.addWidget(alan)
        vbox1.addWidget(alanText)  
        vbox1.addWidget(dal)
        vbox1.addWidget(dalText)
        vbox1.addWidget(egitimYili)
        vbox1.addWidget(egitimYiliText)  
        vbox1.addWidget(isletme)
        vbox1.addWidget(isletmeText)  
        
        gBoxOgrenci.setLayout(vbox1)  
       
        gBoxVeli= QGroupBox("Veli Bilgileri")
        
        adSoyad = QLabel()
        adSoyad.setText("Ad Soyad")
        adSoyadText=QLineEdit()
        
        telefonVeli = QLabel()
        telefonVeli.setText("Telefon")
        telefonVeliText=QLineEdit()
        
        adres = QLabel()
        adres.setText("Adres")
        adresText=QLineEdit()


        
        kaydetButonu=QPushButton('Kaydet') 
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(adSoyad)
        vbox2.addWidget(adSoyadText)
        vbox2.addWidget(telefonVeli)
        vbox2.addWidget(telefonVeliText)
        vbox2.addWidget(adres)
        vbox2.addWidget(adresText)        
        vbox2.addWidget(kaydetButonu)
        
        gBoxVeli.setLayout(vbox2) 
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxOgrenci) 
        mainLayout.addWidget(gBoxVeli) 
        
        
        
        self.setLayout(mainLayout)


class TabIsletme(QWidget):
    def __init__(self):
        super().__init__()
        gBoxIsletme= QGroupBox("İşletme Bilgileri")
        
        isletmeAdi = QLabel()
        isletmeAdi.setText("İşletme Adı")
        isletmeAdiText=QLineEdit()
        
        sinifSube = QLabel()
        sinifSube.setText("Sınıf-Şube")
        sinifSubeText=QLineEdit()
        
        telefonIsletme = QLabel()
        telefonIsletme.setText("Telefon")
        telefonIsletmeText=QLineEdit()
        
        alanIsletme = QLabel()
        alanIsletme.setText("Alan")
        alanIsletmeText=QLineEdit()
                
        dalIsletme = QLabel()
        dalIsletme.setText("Dal")
        dalIsletmeText=QLineEdit()
        
        
        egitimYiliIsletme = QLabel()
        egitimYiliIsletme.setText("Eğitim Yılı")
        egitimYiliIsletmeText=QLineEdit()
        
        
        isletmeIsletme = QLabel()
        isletmeIsletme.setText("İşletme")
        isletmeIsletmeText=QLineEdit()
        
        bulButonu=QPushButton('Bul') 
        
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Al')       
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(isletmeAdi)
        vbox1.addWidget(isletmeAdiText)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)  
        vbox1.addWidget(telefonIsletme)
        vbox1.addWidget(telefonIsletmeText)
        vbox1.addWidget(alanIsletme)
        vbox1.addWidget(alanIsletmeText)  
        vbox1.addWidget(dalIsletme)
        vbox1.addWidget(dalIsletmeText)
        vbox1.addWidget(egitimYiliIsletme)
        vbox1.addWidget(egitimYiliIsletmeText)  
        vbox1.addWidget(isletmeIsletme)
        vbox1.addWidget(isletmeIsletmeText)  
        
        vbox1.addWidget(bulButonu)
        gBoxIsletme.setLayout(vbox1)  
        
        
        gBoxOgrenciler= QGroupBox("Öğrenciler")

        ogrencilerText=QLineEdit() 
        
        kaydetButonu=QPushButton('Kaydet') 
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(ogrencilerText)
        vbox2.addWidget(kaydetButonu)
        gBoxOgrenciler.setLayout(vbox2) 
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxIsletme) 
        mainLayout.addWidget(gBoxOgrenciler) 
        
        
        
        self.setLayout(mainLayout)
class TabRapor(QWidget):
    def __init__(self):
        super().__init__()
        gBoxRapor= QGroupBox("Rapor Bilgileri")
        yil=[]
        for i in range(2020,2051):
            yil.append(i)
        for x in range(0,len(yil)):
            yil[x]=str(yil[x])
        comboYil = QComboBox()
        yilLabel=QLabel("YIL")
        comboYil.addItems(yil)
        #VERİ TABANINDAN ALINMALI ALAN BİLGİLERİ        
        listAlan=["Bilişim Teknolojileri","Elektirik/Elektronik","Makine","Çocuk Gelişim"]        
        comboAlan = QComboBox()
        comboAlan.addItems(listAlan)
        alan=QLabel("Alan")
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Al')       
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(yilLabel)
        vbox1.addWidget(comboYil)
        vbox1.addWidget(alan)
        vbox1.addWidget(comboAlan)       
        vbox1.addWidget(isletmeListesiButonu)
        gBoxRapor.setLayout(vbox1)  
        
        
        gBoxKareKod= QGroupBox("KARE KOD OLUŞTUR")
              
        isletmeAdi = QLabel()
        isletmeAdi.setText("İşletme Adı")
        isletmeAdiText=QLineEdit() 
        isletmeGetirButonu=QPushButton('İşletme Getir') 
        kareKodButonu=QPushButton('Kare Kod oluştur') 
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(isletmeAdi)
        vbox2.addWidget(isletmeAdiText)
        vbox2.addWidget(isletmeGetirButonu)
        vbox2.addWidget(kareKodButonu)
        gBoxKareKod.setLayout(vbox2) 
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxRapor) 
        mainLayout.addWidget(gBoxKareKod) 
        
        
        
        self.setLayout(mainLayout)
class TabGrafik(QWidget):
    def __init__(self):
        super().__init__()
        gBoxGrafik = QGroupBox("Grafik Bilgileri")
        list1=[]
        for i1 in range(2020,2051):
            list1.append(i1)
        for x1 in range(0,len(list1)):
            list1[x1]=str(list1[x1])
        combo1 = QComboBox()
        baslangicYili=QLabel("Başlangıç Yılı")
        combo1.addItems(list1)
        list2=[]
        for i2 in range(2020,2051):
            list2.append(i2)
        for x2 in range(0,len(list2)):
            list2[x2]=str(list2[x2])
        combo2 = QComboBox()
        bitisYili=QLabel("Bitiş Yılı")
        combo2.addItems(list2)
        #VERİ TABANINDAN ALINMALI ALAN BİLGİLERİ   
        listAlan=["Bilişim Teknolojileri","Elektirik/Elektronik","Makine","Çocuk Gelişim"]        
        combo3 = QComboBox()
        combo3.addItems(listAlan)
        alan=QLabel("Alan")
        
        grafikOlusturButonu=QPushButton('Öğrenci Sayılarına Göre İşletme Grafiği Oluştur')       
        grafikOlusturButonu.setGeometry(50, 50, 50, 50)
        
        
        vbox = QVBoxLayout()
        vbox.addWidget(baslangicYili)
        vbox.addWidget(combo1)
        vbox.addWidget(bitisYili)
        vbox.addWidget(combo2)
        vbox.addWidget(alan)
        vbox.addWidget(combo3)
        vbox.addWidget(grafikOlusturButonu)
        gBoxGrafik.setLayout(vbox)   
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(gBoxGrafik)        
        self.setLayout(mainLayout)
        
        
        
        
        
app = QApplication(sys.argv)
tabdialog = Tab()
tabdialog.show()
app.exec()
