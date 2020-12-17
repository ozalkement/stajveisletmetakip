# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:51:47 2020

@author: Şermin
"""


from PyQt5 import QtGui
import os
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.graphics.shapes import *
import pandas as pd
import copy
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#import png
import qrcode
from PIL import Image
import qrcode.image.pil



import matplotlib.pyplot as plt
import pandas as pd


class Tab(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MESLEKİ VE TEKNİK EĞİTİM KURUMLARI STAJ TAKİP YAZILIMI")
        self.setWindowIcon(QIcon("icon.png"))
        #self.setStyleSheet('background-color:grey')
        vbox = QVBoxLayout()
        tabWidget = QTabWidget()
        tabWidget.setFont(QtGui.QFont("Sanserif", 10))
        tabWidget.addTab(TabBilgiEkle(), "Veri Girişleri")
        tabWidget.addTab(TabIsletme(), "İşletme Ekle")
        tabWidget.addTab(TabOgrenci(), "Öğrenci Ekle/Çıkar")
        tabWidget.addTab(TabStaj(), "Staj İşlemleri")         
        tabWidget.addTab(TabRapor(), "Rapor Al")
        tabWidget.addTab(TabGrafik(), "Grafik Oluştur") 
               
        tabWidget.setStyleSheet("background-color: #e0eee0" )
        vbox.addWidget(tabWidget)
        #vbox.addWidget(buttonbox)
        self.setLayout(vbox)
        self.setGeometry(100, 100, 500, 300)
class TabOgrenci(QWidget):
    def __init__(self):
        super().__init__()
        gBoxOgrenci= QGroupBox("Öğrenci Bilgileri")
        gBoxOgrenci.setStyleSheet("font-weight:bold")
        
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
        
        #alan = QLabel()
        #alan.setText("Alan")
        #alanText=QLineEdit()
        
       
       
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboBolum=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            comboBolum.addItems(bolum)
        veritabani.commit()
        
                     
        
        bolum=QLabel("Alan")
        
        
        comboDal=QComboBox()        
        imlec.execute("SELECT dalAdi FROM dal")
        dalListe = imlec.fetchall()
        dalUzunlugu = len(dalListe)
        
        for i in range(0, dalUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            dal = dalListe[i]
            comboDal.addItems(dal)
        veritabani.commit()
        
        dal = QLabel()
        dal.setText("Dal")
        
        
        egitimYili = QLabel()
        egitimYili.setText("Eğitim Yılı")
        yil=[]
        for i in range(2020,2051):
            yil.append(i)
        for x in range(0,len(yil)):
            yil[x]=str(yil[x])
        comboYil = QComboBox()
        yilLabel=QLabel("YIL")
        comboYil.addItems(yil)
        
        
        isletme = QLabel()
        isletme.setText("İşletme")
        comboIsletme=QComboBox()        
        imlec.execute("SELECT isletmeAdi FROM isletmeBilgileri")
        isletmeListe = imlec.fetchall()
        isletmeUzunlugu = len(isletmeListe)
        
        for i in range(0, isletmeUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            isletmeL = isletmeListe[i]
            comboIsletme.addItems(isletmeL)
        veritabani.commit()
        veritabani.close()
        
        
                
        vbox1 = QVBoxLayout()
        vbox1.addWidget(ogrNo)
        vbox1.addWidget(ogrNoText) 
        vbox1.addWidget(ad)
        vbox1.addWidget(adText)
        vbox1.addWidget(soyad)
        vbox1.addWidget(soyadText)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)  
               
        vbox1.addWidget(telefon)
        vbox1.addWidget(telefonText)
        vbox1.addWidget(bolum)
        vbox1.addWidget(comboBolum)
        vbox1.addWidget(dal)
        vbox1.addWidget(comboDal)       
        vbox1.addWidget(egitimYili)
        vbox1.addWidget(comboYil)  
        vbox1.addWidget(isletme)
        vbox1.addWidget(comboIsletme)  
        
        gBoxOgrenci.setLayout(vbox1)  
       
        gBoxVeli= QGroupBox("Veli Bilgileri")
        gBoxVeli.setStyleSheet("font-weight:bold")
        
        adSoyad = QLabel()
        adSoyad.setText("Ad Soyad")
        adSoyadText=QLineEdit()
        
        telefonVeli = QLabel()
        telefonVeli.setText("Telefon")
        telefonVeliText=QLineEdit()
        
        adres = QLabel()
        adres.setText("Adres")
        adresText=QLineEdit()

        #VERİ TABANINA GİRİŞLER
        
        def ogrenciBilgiKayit():
            
           
            
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()
               #--------------------------------------------------
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[comboBolum.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
                #--------------------------------------------------
                veriAlmaDal="SELECT d.dalID FROM dal as d where d.dalAdi=?"
                vDal=[comboBolum.currentText()]
                imlec.execute(veriAlmaDal, vDal)
                dalAdiID = imlec.fetchone()
                dID=str(dalAdiID)
                d = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
                
               
                #--------------------------------------------------
             
        
            sorgu = "INSERT INTO ogrenciBilgileri (ogrNo, ogrAd, ogrSoyad, subeSinif, telefon,egitimYili,veliAdSoyad,veliTelefon,adres,bolumID,dalID) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
           
            veri = [ogrNoText.text(),adText.text(),soyadText.text(),sinifSubeText.text(),telefonText.text(),comboYil.currentText(),adSoyadText.text(),telefonVeliText.text(),adresText.text(),int(b),int(d)]          
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
        
              
  
        
            #VERİ TABANINA GİRİŞLER BİTİMİ
            
          #VERİ TABANI GÜNCELLEME BAŞLANGIÇ
        def ogrenciBilgiGuncelle():
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()
               #--------------------------------------------------
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[comboBolum.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
                #--------------------------------------------------
                veriAlmaDal="SELECT d.dalID FROM dal as d where d.dalAdi=?"
                vDal=[comboBolum.currentText()]
                imlec.execute(veriAlmaDal, vDal)
                dalAdiID = imlec.fetchone()
                dID=str(dalAdiID)
                d = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
                
               
                #--------------------------------------------------
             
        
            sorgu = "UPDATE ogrenciBilgileri set ogrAd=?, ogrSoyad=?, subeSinif=?, telefon=?,egitimYili=?,veliAdSoyad=?,veliTelefon=?,adres=?,bolumID=?,dalID=? where ogrNo=? "
           
            veri = [adText.text(),soyadText.text(),sinifSubeText.text(),telefonText.text(),comboYil.currentText(),adSoyadText.text(),telefonVeliText.text(),adresText.text(),int(b),int(d),ogrNoText.text()]          
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
        
           #VERİ TABANI GÜNCELLEME BİTİŞ
        
        
        
         #VERİ TABANI SİLME BAŞLANGIÇ
        def ogrenciBilgiSilme():
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()
               
             
        
            sorgu = "Delete from ogrenciBilgileri where ogrNo=? "
           
            veri = [ogrNoText.text()]          
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
        
           #VERİ TABANI SİLME BİTİŞ
        
        kaydetButonu=QPushButton('Kaydet') 
        kaydetButonu.setStyleSheet("background-color: #528b8b; font-weight:bold")
        kaydetButonu.clicked.connect(ogrenciBilgiKayit)
        
        guncelleButonu=QPushButton('Güncelle') 
        guncelleButonu.setStyleSheet("background-color: #91F96b; font-weight:bold")
        guncelleButonu.clicked.connect(ogrenciBilgiGuncelle)
        
        silButonu=QPushButton('Sil') 
        silButonu.setStyleSheet("background-color: #916b8b; font-weight:bold")
        silButonu.clicked.connect(ogrenciBilgiSilme)
        
        
        aciklama1 = QLabel()
        aciklama1.setText("DİKKAT!!! Öğrenci bilgileri silme ve güncelleme")
        aciklama2 = QLabel()
        aciklama2.setText("öğrenci numarasına göre yapılmaktadır.")
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(adSoyad)
        vbox2.addWidget(adSoyadText)
        vbox2.addWidget(telefonVeli)
        vbox2.addWidget(telefonVeliText)
        vbox2.addWidget(adres)
        vbox2.addWidget(adresText)        
        vbox2.addWidget(kaydetButonu)
        vbox2.addWidget(aciklama1)
        vbox2.addWidget(aciklama2)
        vbox2.addWidget(guncelleButonu)
        vbox2.addWidget(silButonu)
        gBoxVeli.setLayout(vbox2) 
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxOgrenci) 
        mainLayout.addWidget(gBoxVeli) 
        
        vbox2.addStretch()
        
        self.setLayout(mainLayout)


class TabIsletme(QWidget):
    def __init__(self):
        super().__init__()
        gBoxIsletme= QGroupBox("İşletme Bilgileri")
        gBoxIsletme.setStyleSheet("font-weight:bold")
        
        isletmeAdi = QLabel()
        isletmeAdi.setText("İşletme Adı")
        isletmeAdiText=QLineEdit()
        
        temsilciAdSoyad = QLabel()
        temsilciAdSoyad.setText("Temsilci Adı Soyadı")
        temsilciAdSoyadText=QLineEdit()
        
        telefonIsletme = QLabel()
        telefonIsletme.setText("Telefon")
        telefonIsletmeText=QLineEdit()
        
        ePostaIsletme = QLabel()
        ePostaIsletme.setText("E Posta")
        ePostaIsletmeText=QLineEdit()
        
        vergiNo = QLabel()
        vergiNo.setText("Vergi No")
        vergiNoText=QLineEdit()
        
        
        sgkNo = QLabel()
        sgkNo.setText("SGK No")
        sgkNoText=QLineEdit()
        
        iban = QLabel()
        iban.setText("İBAN")
        ibanText=QLineEdit()
        
        adres = QLabel()
        adres.setText("Adres")
        adresText=QLineEdit()
        
       
        egitimYiliIsletme = QLabel()
        egitimYiliIsletme.setText("Eğitim Yılı")
        yil=[]
        for i in range(2020,2051):
            yil.append(i)
        for x in range(0,len(yil)):
            yil[x]=str(yil[x])
        egitimYiliIsletmeCombo = QComboBox()
        yilLabel=QLabel("YIL")
        egitimYiliIsletmeCombo.addItems(yil)
        
        
        
        
        notu = QLabel()
        notu.setText("Not")
        notuText=QLineEdit()
        

        
       #isletmeBilgileri VERİ TABANINA GİRİŞLER
        
        def isletmeBilgiKayit():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()                             
                sorgu = "INSERT INTO isletmeBilgileri (isletmeAdi,temsilciAdSoyad,telefon,ePosta,vergiNo,sgkNo,adres,iban,tarihZaman,notu) VALUES(?,?,?,?,?,?,?,?,?,?)"
                

                veri = [isletmeAdiText.text(),temsilciAdSoyadText.text(),telefonIsletmeText.text(),ePostaIsletmeText.text(),vergiNoText.text(),sgkNoText.text(),adresText.text(),ibanText.text(),egitimYiliIsletmeText.text(),notuText.text()]          
                imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
                              
        #isletmeBilgileri VERİ TABANINA GİRİŞLER BİTİMİ
        
        
        ekleButonu=QPushButton('İşletme Ekle') 
        ekleButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        ekleButonu.clicked.connect(isletmeBilgiKayit)
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Al')       
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(isletmeAdi)
        vbox1.addWidget(isletmeAdiText)
        vbox1.addWidget(temsilciAdSoyad)
        vbox1.addWidget(temsilciAdSoyadText)  
        vbox1.addWidget(telefonIsletme)
        vbox1.addWidget(telefonIsletmeText)
        vbox1.addWidget(ePostaIsletme)
        vbox1.addWidget(ePostaIsletmeText)        
        vbox1.addWidget(vergiNo)
        vbox1.addWidget(vergiNoText)  
        vbox1.addWidget(sgkNo)
        vbox1.addWidget(sgkNoText)
        vbox1.addWidget(iban)
        vbox1.addWidget(ibanText)  
        vbox1.addWidget(adres)
        vbox1.addWidget(adresText) 
        vbox1.addWidget(egitimYiliIsletme)
        vbox1.addWidget(egitimYiliIsletmeCombo)
        vbox1.addWidget(notu)
        vbox1.addWidget(notuText) 
        
        
        vbox1.addWidget(ekleButonu)
        gBoxIsletme.setLayout(vbox1)  
        
        

        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxIsletme) 

        
        
        
        self.setLayout(mainLayout)
        
        
class TabStaj(QWidget):
    def __init__(self):
        super().__init__()
        gBoxIsletme= QGroupBox("İşletme Bilgileri")
        gBoxIsletme.setStyleSheet("font-weight:bold;")
        
        isletmeAdi = QLabel()
        isletmeAdi.setText("İşletme Adı")
        
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboIsletme=QComboBox()        
        imlec.execute("SELECT isletmeAdi FROM isletmeBilgileri")
        isletmeListe = imlec.fetchall()
        isletmeUzunlugu = len(isletmeListe)
        
        for i in range(0, isletmeUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            isletmeL = isletmeListe[i]
            comboIsletme.addItems(isletmeL)
        veritabani.commit()
        
        
        
        
        
        
        sinifSube = QLabel()
        sinifSube.setText("Sınıf-Şube")

        sinifSubeCombo=QComboBox()        
        imlec.execute("SELECT subeSinif FROM dal")
        sinifListe = imlec.fetchall()
        sinifUzunlugu = len(sinifListe)
        
        for i in range(0, sinifUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            sinif = sinifListe[i]
            sinifSubeCombo.addItems(sinif)
        veritabani.commit()
        
        
        alanIsletme = QLabel()
        alanIsletme.setText("Alan")
        
        
        alanIsletmeText=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            alanIsletmeText.addItems(bolum)
        veritabani.commit()
        
        
                
        dalIsletme = QLabel()
        dalIsletme.setText("Dal")
        dalIsletmeText=QComboBox()        
        imlec.execute("SELECT dalAdi FROM dal")
        dalListe = imlec.fetchall()
        dalUzunlugu = len(dalListe)
        
        for i in range(0, dalUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            dal = dalListe[i]
            dalIsletmeText.addItems(dal)
        veritabani.commit()
        
        
        egitimYiliIsletme = QLabel()
        egitimYiliIsletme.setText("Eğitim Yılı")
        yil=[]
        for i in range(2020,2051):
            yil.append(i)
        for x in range(0,len(yil)):
            yil[x]=str(yil[x])
        egitimYiliIsletmeCombo = QComboBox()
        yilLabel=QLabel("YIL")
        egitimYiliIsletmeCombo.addItems(yil)
        
        donem = QLabel()
        donem.setText("Dönemi")
        donemText=QLineEdit()
        

        
        #bulButonu=QPushButton('Bul') 
        #bulButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Al')       
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(isletmeAdi)
        vbox1.addWidget(comboIsletme)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeCombo)          
        vbox1.addWidget(alanIsletme)
        vbox1.addWidget(alanIsletmeText)  
        vbox1.addWidget(dalIsletme)
        vbox1.addWidget(dalIsletmeText)
        vbox1.addWidget(egitimYiliIsletme)
        vbox1.addWidget(egitimYiliIsletmeCombo) 
        vbox1.addWidget(donem)
        vbox1.addWidget(donemText)
         
        
        #vbox1.addWidget(bulButonu)
        gBoxIsletme.setLayout(vbox1)  
        
        
        gBoxOgrenciler= QGroupBox("Öğrenciler")
        gBoxOgrenciler.setStyleSheet("font-weight:bold")

        ogrencilerText=QListWidget()
        
        #---------ÖĞRENCİ LİSTELEME---------
        def ogrenciListele():
            imlec = veritabani.cursor()
            veriAlmaOgrenci="SELECT ogrAd, ogrSoyad FROM ogrenciBilgileri o , isletmeBilgileri i,bolum b, dal d, stajBilgileri s where o.bolumID=b.bolumID and o.dalID=d.dalID and d.bolumID=b.bolumID and i.isletmeID=s.isletmeID and isletmeAdi=? and d.subeSinif=? and bolumAdi=? and dalAdi=?"                   
            vOgrenci=[comboIsletme.currentText(),sinifSubeCombo.currentText(),alanIsletmeText.currentText(),dalIsletmeText.currentText()]
            imlec.execute(veriAlmaOgrenci, vOgrenci)
            ogrenciAdSoyad = imlec.fetchall()
            oAdSoyad=str(ogrenciAdSoyad) 
            adSoyadOgr = oAdSoyad.replace(",","").replace("(","").replace(")","").replace("'","") 
            print(adSoyadOgr)
            imlec = veritabani.cursor()
            veritabani.commit()
            #listAlan=[]
            #for x in adSoyadOgr:
                #listAlan.append(x)
                
            #print(listAlan)
            ogrencilerText.addItem(adSoyadOgr)

            
            
                

        #---------ÖĞRENCİ LİSTELEME---------
        
        
        
        
        
        listeleButonu=QPushButton('Listele') 
        listeleButonu.setStyleSheet("background-color: #528b8b; font-weight:bold")
        listeleButonu.clicked.connect(ogrenciListele)
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(ogrencilerText)
        vbox2.addWidget(listeleButonu)
        gBoxOgrenciler.setLayout(vbox2) 
        
        vbox2.addStretch()
        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxIsletme) 
        mainLayout.addWidget(gBoxOgrenciler) 
        
        
        
        self.setLayout(mainLayout)        
        
        
        
        
        
        
        
        
class TabRapor(QWidget):
    def __init__(self):
        super().__init__()
        gBoxRapor= QGroupBox("Rapor Bilgileri")
        gBoxRapor.setStyleSheet("font-weight:bold")
        
        yil=[]
        for i in range(2020,2051):
            yil.append(i)
        for x in range(0,len(yil)):
            yil[x]=str(yil[x])
        comboYil = QComboBox()
        yilLabel=QLabel("YIL")
        comboYil.addItems(yil)
        
        #VERİ TABANINDAN ALINMALI ALAN BİLGİLERİ        
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboAlan=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            comboAlan.addItems(bolum)
        veritabani.commit()
        
        alan=QLabel("Alan")
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Al') 
        isletmeListesiButonu.setStyleSheet("background-color: #6e8b3d; font-weight:bold")
        
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(yilLabel)
        vbox1.addWidget(comboYil)
        vbox1.addWidget(alan)
        vbox1.addWidget(comboAlan)       
        vbox1.addWidget(isletmeListesiButonu)
        gBoxRapor.setLayout(vbox1)  
        
        
        gBoxKareKod= QGroupBox("KARE KOD OLUŞTUR")
        gBoxKareKod.setStyleSheet("font-weight:bold")
              
        isletmeAdi = QLabel()
        isletmeAdi.setText("İşletme Adı")
        
        
        
         #VERİ TABANINDAN İŞLETME AD ALINMA 
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        isletmeAdiCombo=QComboBox()        
        imlec.execute("SELECT isletmeAdi FROM isletmeBilgileri")
        isletmeListe = imlec.fetchall()
        isletmeUzunlugu = len(isletmeListe)
        
        for i in range(0, isletmeUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            isletme = isletmeListe[i]
            isletmeAdiCombo.addItems(isletme)
        veritabani.commit()
        
        
      
        
        isletmeGetirButonu=QPushButton('İşletme Getir')
        isletmeGetirButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        
        
        
        #KARE KOD OLUŞTURMA FONKSİYONU BAŞLANGIÇ
        def kareKod():
        
    
            pdfmetrics.registerFont(TTFont('Montserrat-Bold',"fonts\\Montserrat-Bold.ttf"))
            pdfmetrics.registerFont(TTFont('Montserrat-Regular',"fonts\\Montserrat-Regular.ttf"))
            pdfmetrics.registerFont(TTFont('Montserrat-Light',"fonts\\Montserrat-Light.ttf"))
            pdfmetrics.registerFont(TTFont('Montserrat-LightItalic',"fonts\\Montserrat-LightItalic.ttf"))
            pdfmetrics.registerFont(TTFont('Montserrat-Black',"fonts\\Montserrat-Black.ttf"))
    
    
            
            # PDF ayarla
            packet = io.BytesIO()
            
            kart_boyutu = (3.54, 5.31)
            kanvas = canvas.Canvas(packet, pagesize=kart_boyutu)
            
            isletmeKareKod =isletmeAdiCombo.currentText()
            
            
    
            # QR Code Kısmı
               
            qr = qrcode.QRCode(version=1,box_size=1.3,border=2)
            qr.add_data("{} ".format(isletmeKareKod))
            qr.make(fit=True)
            img = qr.make_image(image_factory= qrcode.image.pil.PilImage, fill_color='black', back_color='white')
            img = img.resize((64,64), Image.ANTIALIAS)
            img.save('qrcode{}.png'.format(isletmeKareKod))
            kanvas.drawImage('qrcode{}.png'.format(isletmeKareKod),1.3*inch,1.3*inch)
            kanvas.showPage()

            kanvas.save()
    
            # PDF'yi kaydet
            packet.seek(0)
            canvas_pdf = PdfFileReader(packet)
            bos_sayfa = PdfFileReader(open("bosSayfa.pdf",'rb'))
            
            output = PdfFileWriter()
        
            for i in range(canvas_pdf.getNumPages()):
                page = copy.copy(bos_sayfa.getPage(0))
                page.mergePage(canvas_pdf.getPage(i))
                output.addPage(page)
                print("{}. işletme bilgileri oluşturuldu.".format(i))
    
            with open("isletmeBilgileri.pdf","wb") as outfile:
                output.write(outfile)
      
        #KARE KOD OLUŞTURMA FONKSİYONU BİTİŞ
        
        
        
        kareKodButonu=QPushButton('Kare Kod oluştur') 
        kareKodButonu.setStyleSheet("background-color: #528b8b; font-weight:bold")
        
        kareKodButonu.clicked.connect(kareKod)
        
        
        
        
        
        
        vbox2 = QVBoxLayout()  
        vbox2.addWidget(isletmeAdi)
        vbox2.addWidget(isletmeAdiCombo)
        vbox2.addWidget(isletmeGetirButonu)
        vbox2.addWidget(kareKodButonu)
        gBoxKareKod.setLayout(vbox2) 
        
        vbox2.addStretch()
        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxRapor) 
        mainLayout.addWidget(gBoxKareKod) 
        
        
        
        self.setLayout(mainLayout)
class TabGrafik(QWidget):
    def __init__(self):
        super().__init__()
        gBoxGrafik = QGroupBox("Grafik Bilgileri")
        gBoxGrafik.setStyleSheet("font-weight:bold")
        
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
        
        listAlan=[]
        
         #VERİ TABANI BİLGİ ALIMI BAŞLANGI
        veritabani = 'stajIsletme.sqlite'
        dosya_var_mi = os.path.exists(veritabani)
        if dosya_var_mi:
                    veritabani = sqlite3.connect(veritabani)
                    imlec = veritabani.cursor() 
                    sorgu = " SELECT bolumAdi FROM bolum"          
                    imlec.execute(sorgu)
                    bolumler=imlec.fetchall()
                    for x in bolumler:
                        listAlan.append(x[0])
                        #print(listAlan)
                    veritabani.commit()
                    veritabani.close()
        
        def bolumyilisletmegrafik():
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                    veritabani = sqlite3.connect(veritabani)
                    imlec = veritabani.cursor() 
                    sorgu = " SELECT isl.isletmeAdi as isletmeadi,count() as ogrencisayisi FROM stajBilgileri st,isletmeBilgileri isl WHERE (egitimyili BETWEEN ? AND ?) AND st.isletmeID ==isl.isletmeID  GROUP BY st.isletmeID  "               
                    veri = [combo1.currentText(),combo2.currentText()]            
                    imlec.execute(sorgu, veri)
                    df = pd.DataFrame(imlec.fetchall())
                    print(df)
                    df.columns = ['firma', 'sayi']
                    #df.index = ['firma', 'sayi']
                    print("Yeni Hali")
                    print(df)
                    #ax = df.plot(kind='bar', title ="İşletme Başı Öğrenci Sayısı", figsize=(10, 6), legend=True, fontsize=12)
                    #ax.set_xlabel("İşletme İsmi", fontsize=12)
                    #ax.set_ylabel("Öğrenci Sayısı", fontsize=12)
                    #plt.show()
                    df.plot.bar(x="firma", y="sayi", rot=0, title="İşletme Başı Öğrenci Sayısı")
                    plt.show()
                
                    veritabani.commit()
                    veritabani.close()               
        
        #VERİTABANI BİLGİ ALIMI BİTİŞ
        
        
        
        
        

        
        
        
        #VERİ TABANINDAN ALINMALI ALAN BİLGİLERİ   
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboAlan=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            comboAlan.addItems(bolum)
        veritabani.commit()
        alan=QLabel("Alan")
        
        grafikOlusturButonu=QPushButton('Öğrenci Sayılarına Göre İşletme Grafiği Oluştur')
        grafikOlusturButonu.setStyleSheet("background-color: #6e8b3d; font-weight:bold")
        grafikOlusturButonu.setGeometry(50, 50, 50, 50)
        grafikOlusturButonu.clicked.connect(bolumyilisletmegrafik)
        
        
        
        vbox = QVBoxLayout()
        vbox.addWidget(baslangicYili)
        vbox.addWidget(combo1)
        vbox.addWidget(bitisYili)
        vbox.addWidget(combo2)
        vbox.addWidget(alan)
        vbox.addWidget(comboAlan)
        vbox.addWidget(grafikOlusturButonu)
        vbox.addStretch()
        
        gBoxGrafik.setLayout(vbox)   
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(gBoxGrafik)        
        self.setLayout(mainLayout)
        
        
class TabBilgiEkle(QWidget):
    def __init__(self):
        super().__init__()
        gBoxBolumDal= QGroupBox("Bölüm ve Dal Bilgileri")
        gBoxBolumDal.setStyleSheet("font-weight:bold")
        
        sinifSube = QLabel()
        sinifSube.setText("Sınıf-Şube")
        sinifSubeText=QLineEdit()
        
        alanIsletme = QLabel()
        alanIsletme.setText("Bölüm")
        alanIsletmeText=QLineEdit()
        
        #BÖLÜM VERİ TABANINA GİRİŞLER
        
        def bolumBilgiKayit():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()                             
                sorgu = "INSERT INTO bolum (bolumAdi) VALUES(?)"
                veri = [alanIsletmeText.text()]          
                imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
                              
        #BÖLÜM VERİ TABANINA GİRİŞLER BİTİMİ
        
        ekleBolumButonu=QPushButton('Bölüm Ekle')
        ekleBolumButonu.setStyleSheet("background-color: #b7ff55; font-weight:bold")
        ekleBolumButonu.clicked.connect(bolumBilgiKayit)
                
        dalIsletme = QLabel()
        dalIsletme.setText("Dal")
        dalIsletmeText=QLineEdit()
        
        bolumD = QLabel()
        bolumD.setText("Bölüm")
        
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboBolum=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            comboBolum.addItems(bolum)
        veritabani.commit()
        #DAL VERİ TABANINA GİRİŞLER
        
        def dalBilgiKayit():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[comboBolum.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
       
            sorgu = "INSERT INTO dal (dalAdi,bolumID,subeSinif) VALUES(?,?,?)"
            veri = [dalIsletmeText.text(),int(b),sinifSubeText.text()] 
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
                          
                              
        #DAL VERİ TABANINA GİRİŞLER BİTİMİ
        
        
        ekleDalButonu=QPushButton('Dal Ekle')
        ekleDalButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        ekleDalButonu.clicked.connect(dalBilgiKayit)
        
               
        vbox1 = QVBoxLayout()           
         
        vbox1.addWidget(alanIsletme)
        vbox1.addWidget(alanIsletmeText)
        vbox1.addWidget(ekleBolumButonu)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)
        vbox1.addWidget(bolumD)
        vbox1.addWidget(comboBolum)
        vbox1.addWidget(dalIsletme)
        vbox1.addWidget(dalIsletmeText)
        
        
        vbox1.addWidget(ekleDalButonu)
        gBoxBolumDal.setLayout(vbox1)  
        
        
        gBoxOgretmen= QGroupBox("Koordinatör Öğretmen Bilgileri")
        gBoxOgretmen.setStyleSheet("font-weight:bold")

        adOrt = QLabel()
        adOrt.setText("Ad")
        adOrtText=QLineEdit()
        
        soyadOgrt = QLabel()
        soyadOgrt.setText("Soyad")
        soyadOgrtText=QLineEdit()
        
        
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        alanText=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            #bolumListe = list(map(str, bolumListe))
            bolum = bolumListe[i]
            alanText.addItems(bolum)
        veritabani.commit()  
        
        
        def ogretmenBilgiKayit():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[alanText.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                imlec = veritabani.cursor()
       
            sorgu = "INSERT INTO koordinatorOgretmen (ogrtAd,ogrtSoyad,bolumID) VALUES(?,?,?)"
            veri = [adOrtText.text(),soyadOgrtText.text(),int(b)] 
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
                          
                              
        #ÖĞRETMEN VERİ TABANINA GİRİŞLER BİTİMİ
        
     
        
        alanOrt=QLabel("Alan")

        
        ekleOgrtButonu=QPushButton('Öğretmen Ekle') 
        ekleOgrtButonu.setStyleSheet("background-color: #528b8b; font-weight:bold")
        ekleOgrtButonu.clicked.connect(ogretmenBilgiKayit)
        vbox2 = QVBoxLayout()  
            
        vbox2.addWidget(adOrt)
        vbox2.addWidget(adOrtText)
        vbox2.addWidget(soyadOgrt)
        vbox2.addWidget(soyadOgrtText)               
        vbox2.addWidget(alanOrt)
        vbox2.addWidget(alanText)
        vbox2.addWidget(ekleOgrtButonu)
        gBoxOgretmen.setLayout(vbox2) 
        
        vbox2.addStretch()
        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxBolumDal) 
        mainLayout.addWidget(gBoxOgretmen) 
        
        
        
        self.setLayout(mainLayout)        
        


        
app = QApplication(sys.argv)
vt = sqlite3.connect('stajIsletme.sqlite')
im = vt.cursor()
            
sorguBolum= """CREATE TABLE IF NOT EXISTS "bolum" ("bolumID"	INTEGER ,	
"bolumAdi"	TEXT, 	PRIMARY KEY("bolumID" AUTOINCREMENT))"""

im.execute(sorguBolum)
                
sorguDal= """CREATE TABLE IF NOT EXISTS  "dal" ("dalID"	INTEGER ,	
	"dalAdi"	TEXT,
	"bolumID"	INTEGER,
    "subeSinif"	TEXT,
	PRIMARY KEY("dalID" AUTOINCREMENT),
	CONSTRAINT "bolumDalFK" FOREIGN KEY("bolumID") REFERENCES "bolum"("bolumID")
)"""
	
       
im.execute(sorguDal)  



sorguIl= """CREATE TABLE IF NOT EXISTS "il" (
	"ilID"	INTEGER ,
	"ilAdi"	TEXT,
	PRIMARY KEY("ilID")
) """
	
im.execute(sorguIl)  


sorguIsletme= """CREATE TABLE IF NOT EXISTS "isletmeBilgileri" (
	"isletmeID"	INTEGER ,
	"isletmeAdi"	TEXT,
	"temsilciAdSoyad"	TEXT,
	"telefon"	TEXT,
	"ePosta"	TEXT,
	"vergiNo"	INTEGER,
	"sgkNo"	INTEGER,
	"adres"	TEXT,
	"il"	INTEGER,
	"iban"	TEXT,
	"tarihZaman"	TEXT,
	"notu"	TEXT,
	CONSTRAINT "isletmeIlFK" FOREIGN KEY("il") REFERENCES "il"("ilID"),
	CONSTRAINT "isletmeIDPK" PRIMARY KEY("isletmeID" AUTOINCREMENT)
) """
	
im.execute(sorguIsletme)  





sorguOgretmen= """CREATE TABLE IF NOT EXISTS "koordinatorOgretmen" (
	"ogrtmenID"	INTEGER ,
	"ogrtAd"	TEXT,
	"ogrtSoyad"	TEXT,
	"bolumID"	INTEGER,
	FOREIGN KEY("bolumID") REFERENCES "bolum"("bolumID"),
	PRIMARY KEY("ogrtmenID" AUTOINCREMENT)
) """
	
im.execute(sorguOgretmen)  
             
            
sorguOgrenci = """ CREATE TABLE IF NOT EXISTS "ogrenciBilgileri" 
            ( "ogrNo" INTEGER , "tcNo" INTEGER UNIQUE, "ogrAd" TEXT, 
             "ogrSoyad" TEXT, "subeSinif" TEXT, "telefon" TEXT, 
             "egitimYili" TEXT, "veliAdSoyad" TEXT, "veliTelefon" TEXT, 
             "adres" TEXT, "il" INTEGER, "bolumID" INTEGER, 
             "dalID" INTEGER, CONSTRAINT "ogrNoFK" PRIMARY KEY("ogrNo"),
             CONSTRAINT "ogrenciDalFK" FOREIGN KEY("dalID") REFERENCES "dal"("dalID"), 
             CONSTRAINT "ogrenciIlFK" FOREIGN KEY("il") REFERENCES "il"("ilID"), 
             CONSTRAINT "ogrenciBolumFK" FOREIGN KEY("bolumID") REFERENCES "bolum"("bolumID") )"""
 
            
im.execute(sorguOgrenci)            
            
sorguStaj = """  CREATE TABLE IF NOT EXISTS "stajBilgileri" (
	"stajID" INTEGER,
	"egitimYili"	INTEGER,
	"donem"	INTEGER,
	"isletmeID"	INTEGER,
	"bolumID"	INTEGER,
	"dalID"	INTEGER,
	"ogretmenID"	INTEGER,
	"tarihZaman"	TEXT,
	CONSTRAINT "stajPK" PRIMARY KEY("stajID" AUTOINCREMENT) ,
	CONSTRAINT "stajBolumFK" FOREIGN KEY("bolumID") REFERENCES "bolum"("bolumID"),
	CONSTRAINT "stajOgrtFK" FOREIGN KEY("ogretmenID") REFERENCES "koordinatorOgretmen"("ogrtmenID"),
	CONSTRAINT "stajIsletmeFK" FOREIGN KEY("isletmeID") REFERENCES "isletmeBilgileri"("isletmeID"),
	CONSTRAINT "stajDalFK" FOREIGN KEY("dalID") REFERENCES "dal"("dalID")
) """         
            
im.execute(sorguStaj)             
vt.commit()
           

tabdialog = Tab()
tabdialog.show()
app.exec()
