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
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)


import matplotlib.pyplot as plt
import pandas as pd


import stajIsletme



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
        
       
        
        self.setLayout(vbox)
        self.setGeometry(100, 100, 700, 300)
        
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
        
        bolumSirasi = QLabel()
        bolumSirasi.setText("Bölüm Sırasını giriniz:")
        bolumSirasiText=QLineEdit()
        
        bolumSil=QPushButton('Bölüm Sil')
        bolumSil.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------BÖLÜM VERİ TABANI SİLME BAŞLANGIÇ--------------
        def bolumBilgiSilme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                   
                sorgu = "DELETE FROM bolum where bolumID=?"
                veri = [bolumSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------BÖLÜM VERİ TABANI SİLME BİTİŞ--------------
        bolumSil.clicked.connect(bolumBilgiSilme)
        bolumGuncelle=QPushButton('Bölüm Güncelle')
        bolumGuncelle.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------BÖLÜM VERİ TABANI Güncelleme BAŞLANGIÇ--------------
        def bolumBilgiGuncelleme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                   
                sorgu = "UPDATE bolum SET bolumAdi=? where bolumID=?"
                veri = [alanIsletmeText.text(),bolumSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------BÖLÜM VERİ TABANI Güncelleme BİTİŞ--------------
        
        
        bolumGuncelle.clicked.connect(bolumBilgiGuncelleme)
        
        gBoxsilmeGuncellemeBolumVeri= QGroupBox()      
        silmeGuncellemeBolumH= QHBoxLayout()
        silmeGuncellemeBolumH.addWidget(bolumSirasi)
        silmeGuncellemeBolumH.addWidget(bolumSirasiText)
        gBoxsilmeGuncellemeBolumButon= QGroupBox()
        silmeGuncellemeBolumH2= QHBoxLayout()
        silmeGuncellemeBolumH2.addWidget(bolumSil)
        silmeGuncellemeBolumH2.addWidget(bolumGuncelle)
        
        
        
        
        #------------------BÖLÜM VERİ TABANINA GİRİŞLER----------------------------

    
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
        
        
        #------VERİ TABANI BOLUM TABLO GÖRÜNME BAŞLANGIÇ---------
        
        veriListesi = QTableWidget()
        veriDalListesi = QTableWidget()
        veriOgrtListesi = QTableWidget()
        def yenile():
            veritabani = 'stajIsletme.sqlite'  
            veritabani = sqlite3.connect(veritabani)
            imlec = veritabani.cursor()              
            veriListesi.setAlternatingRowColors(True)
            veriListesi.setColumnCount(2)
            veriListesi.horizontalHeader().setCascadingSectionResizes(False)
            veriListesi.horizontalHeader().setSortIndicatorShown(False)
            veriListesi.horizontalHeader().setStretchLastSection(True)
            veriListesi.verticalHeader().setVisible(False)
            veriListesi.verticalHeader().setCascadingSectionResizes(False)
            veriListesi.verticalHeader().setStretchLastSection(False)
            veriListesi.setHorizontalHeaderLabels(("Bölüm Sırası", "Bölüm Adı"))
            veriListesi.setMinimumSize(300,100)                    
            veri = imlec.execute("SELECT * FROM bolum")
            veri = veri.fetchall()
            veriListesi.setRowCount(0)
            for satirSayisi, satirVerisi in enumerate(veri):
                veriListesi.insertRow(satirSayisi)
                for sutunSayisi, sutunVeri in enumerate(satirVerisi):
                    print(sutunSayisi,sutunVeri)
                    veriListesi.setItem(satirSayisi,sutunSayisi,QTableWidgetItem(str(sutunVeri)))
            veritabani.commit()
            veriDalListesi.setAlternatingRowColors(True)
            veriDalListesi.setColumnCount(2)
            veriDalListesi.horizontalHeader().setCascadingSectionResizes(False)
            veriDalListesi.horizontalHeader().setSortIndicatorShown(False)
            veriDalListesi.horizontalHeader().setStretchLastSection(True)
            veriDalListesi.verticalHeader().setVisible(False)
            veriDalListesi.verticalHeader().setCascadingSectionResizes(False)
            veriDalListesi.verticalHeader().setStretchLastSection(False)
            veriDalListesi.setHorizontalHeaderLabels(("Dal Sırası", "Dal Adı"))
            veriDalListesi.setMinimumSize(300,100)                    
            veriDal = imlec.execute("SELECT dalID, dalAdi FROM dal")
            veriDal = veriDal.fetchall()
            veriDalListesi.setRowCount(0)
            for satirSayisiD, satirVerisiD in enumerate(veriDal):
                veriDalListesi.insertRow(satirSayisiD)
                for sutunSayisiD, sutunVeriD in enumerate(satirVerisiD):
                    print(sutunSayisiD,sutunVeriD)
                    veriDalListesi.setItem(satirSayisiD,sutunSayisiD,QTableWidgetItem(str(sutunVeriD)))
            veritabani.commit()
            veriOgrtListesi.setAlternatingRowColors(True)
            veriOgrtListesi.setColumnCount(3)
            veriOgrtListesi.horizontalHeader().setCascadingSectionResizes(False)
            veriOgrtListesi.horizontalHeader().setSortIndicatorShown(False)
            veriOgrtListesi.horizontalHeader().setStretchLastSection(True)
            veriOgrtListesi.verticalHeader().setVisible(False)
            veriOgrtListesi.verticalHeader().setCascadingSectionResizes(False)
            veriOgrtListesi.verticalHeader().setStretchLastSection(False)
            veriOgrtListesi.setHorizontalHeaderLabels(("Öğretmen Sırası", "Ad","Soyad"))
            veriOgrtListesi.setMinimumSize(400,100)                    
            veriOgrt = imlec.execute("SELECT ogrtmenID,ogrtAd,ogrtSoyad FROM koordinatorOgretmen")
            veriOgrt = veriOgrt.fetchall()
            veriOgrtListesi.setRowCount(0)
            for satirSayisiOgrt, satirVerisiOgrt in enumerate(veriOgrt):
                veriOgrtListesi.insertRow(satirSayisiOgrt)
                for sutunSayisiOgrt, sutunVeriOgrt in enumerate(satirVerisiOgrt):
                    print(sutunSayisiOgrt,sutunVeriOgrt)
                    veriOgrtListesi.setItem(satirSayisiOgrt,sutunSayisiOgrt,QTableWidgetItem(str(sutunVeriOgrt)))
            veritabani.commit()    
        yenileButonu=QPushButton('Tabloları Yenile')
        yenileButonu.setStyleSheet("background-color: #ff0000; font-weight:bold")
        yenileButonu.clicked.connect(yenile)
               
                
        #------VERİ TABANI TABLO GÖRÜNME BİTİŞ---------
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
        
        dalSirasi = QLabel()
        dalSirasi.setText("Dal Sırasını giriniz:")
        dalSirasiText=QLineEdit()
        
        dalSil=QPushButton('Dal Sil')
        dalSil.setStyleSheet("background-color: #777; font-weight:bold")
        #-------------DAL VERİ TABANI SİLME BAŞLANGIÇ--------------
        def dalBilgiSilme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                   
                sorgu = "DELETE FROM dal where dalID=?"
                veri = [dalSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------DAL VERİ TABANI SİLME BİTİŞ--------------
        dalSil.clicked.connect(dalBilgiSilme)
        dalGuncelle=QPushButton('Dal Güncelle')
        dalGuncelle.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------Dal VERİ TABANI Güncelleme BAŞLANGIÇ--------------
        def dalBilgiGuncelleme():                                  
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
                   
            sorgu = "UPDATE dal SET dalAdi=?,bolumID=?,subeSinif=? where dalID=?"
            veri = [dalIsletmeText.text(),int(b),sinifSubeText.text(),dalSirasiText.text()] 
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()        
        
        #-------------Dal VERİ TABANI Güncelleme BİTİŞ--------------
        dalGuncelle.clicked.connect(dalBilgiGuncelleme)
        
        gBoxsilmeGuncellemeDalVeri= QGroupBox()
        silmeGuncellemeDalH= QHBoxLayout()
        silmeGuncellemeDalH.addWidget(dalSirasi)
        silmeGuncellemeDalH.addWidget(dalSirasiText)
        gBoxsilmeGuncellemeDalButon= QGroupBox()
        silmeGuncellemeDalH2= QHBoxLayout()
        silmeGuncellemeDalH2.addWidget(dalSil)
        silmeGuncellemeDalH2.addWidget(dalGuncelle)
        
        
        
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
                          
                              
        #------------------DAL VERİ TABANINA GİRİŞLER BİTİMİ----------
        
        
        ekleDalButonu=QPushButton('Dal Ekle')
        ekleDalButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        ekleDalButonu.clicked.connect(dalBilgiKayit)
        
             
        vbox1 = QVBoxLayout()           
        
        
        
        
        vbox1.addWidget(alanIsletme)
        vbox1.addWidget(alanIsletmeText)
        vbox1.addWidget(ekleBolumButonu)
        vbox1.addWidget(gBoxsilmeGuncellemeBolumVeri)
        gBoxsilmeGuncellemeBolumVeri.setLayout(silmeGuncellemeBolumH)
        vbox1.addStretch()
        vbox1.addWidget(gBoxsilmeGuncellemeBolumButon)
        gBoxsilmeGuncellemeBolumButon.setLayout(silmeGuncellemeBolumH2)
        vbox1.addWidget(veriListesi)
        
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeText)
        vbox1.addWidget(bolumD)
        vbox1.addWidget(comboBolum)
        vbox1.addWidget(dalIsletme)
        vbox1.addWidget(dalIsletmeText)
        
        
        vbox1.addWidget(ekleDalButonu)
        
        vbox1.addWidget(veriDalListesi)
        vbox1.addWidget(gBoxsilmeGuncellemeDalVeri)
        gBoxsilmeGuncellemeDalVeri.setLayout(silmeGuncellemeDalH)
        vbox1.addWidget(gBoxsilmeGuncellemeDalButon)
        gBoxsilmeGuncellemeDalButon.setLayout(silmeGuncellemeDalH2)
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
                          
                              
        #-------------ÖĞRETMEN VERİ TABANINA GİRİŞLER BİTİMİ--------------
        
       
        
        alanOrt=QLabel("Alan")

        
        ekleOgrtButonu=QPushButton('Öğretmen Ekle') 
        ekleOgrtButonu.setStyleSheet("background-color: #528b8b; font-weight:bold")
        ekleOgrtButonu.clicked.connect(ogretmenBilgiKayit)
        
        ogrtSirasi = QLabel()
        ogrtSirasi.setText("Öğretmen Sırasını giriniz:")
        ogrtSirasiText=QLineEdit()
        
        ogrtSil=QPushButton('Öğretmen Sil')
        ogrtSil.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------ÖĞRETMEN VERİ TABANI SİLME BAŞLANGIÇ--------------
        def ogretmenBilgiSilme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                   
                sorgu = "DELETE FROM koordinatorOgretmen where ogrtmenID=?"
                veri = [ogrtSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------ÖĞRETMEN VERİ TABANI SİLME BİTİŞ--------------
        ogrtSil.clicked.connect(ogretmenBilgiSilme)
        ogrtGuncelle=QPushButton('Öğretmen Güncelle')
        ogrtGuncelle.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------ÖĞRETMEN VERİ TABANI Güncelleme BAŞLANGIÇ--------------
        def ogrtBilgiGuncelleme():                                  
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
                   
                sorgu = "UPDATE koordinatorOgretmen SET ogrtAd=?,ogrtSoyad=?,bolumID=? where ogrtmenID=?"
                veri = [adOrtText.text(),soyadOgrtText.text(),int(b),ogrtSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------ÖĞRETMEN VERİ TABANI Güncelleme BİTİŞ--------------
        ogrtGuncelle.clicked.connect(ogrtBilgiGuncelleme)
        
        gBoxsilmeGuncellemeOgrtVeri= QGroupBox()
        silmeGuncellemeOgrtH= QHBoxLayout()
        silmeGuncellemeOgrtH.addWidget(ogrtSirasi)
        silmeGuncellemeOgrtH.addWidget(ogrtSirasiText)
        gBoxsilmeGuncellemeOgrtButon= QGroupBox()
        silmeGuncellemeOgrtH2= QHBoxLayout()
        silmeGuncellemeOgrtH2.addWidget(ogrtSil)
        silmeGuncellemeOgrtH2.addWidget(ogrtGuncelle)
        
       
        
        vbox2 = QVBoxLayout()  
            
        vbox2.addWidget(adOrt)
        vbox2.addWidget(adOrtText)
        vbox2.addWidget(soyadOgrt)
        vbox2.addWidget(soyadOgrtText)               
        vbox2.addWidget(alanOrt)
        vbox2.addWidget(alanText)
        vbox2.addWidget(ekleOgrtButonu)
        vbox2.addWidget(gBoxsilmeGuncellemeOgrtVeri)
        gBoxsilmeGuncellemeOgrtVeri.setLayout(silmeGuncellemeOgrtH)
        vbox2.addWidget(gBoxsilmeGuncellemeOgrtButon)
        gBoxsilmeGuncellemeOgrtButon.setLayout(silmeGuncellemeOgrtH2)
        vbox2.addWidget(veriOgrtListesi)
        vbox2.addWidget(yenileButonu)
        gBoxOgretmen.setLayout(vbox2) 
        
        vbox2.addStretch()
        vbox1.addStretch()
        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxBolumDal) 
        mainLayout.addWidget(gBoxOgretmen) 
        
        
        
        self.setLayout(mainLayout)  
        yenile()
        
        
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
    
       
        veritabani = 'stajIsletme.sqlite'           
        veritabani = sqlite3.connect(veritabani)
        imlec = veritabani.cursor()
        comboBolum=QComboBox()        
        imlec.execute("SELECT bolumAdi FROM bolum")
        bolumListe = imlec.fetchall()
        bolumUzunlugu = len(bolumListe)
        
        for i in range(0, bolumUzunlugu):
            bolum = bolumListe[i]
            comboBolum.addItems(bolum)
        veritabani.commit()                                    
        bolum=QLabel("Alan")
        
        
        comboDal=QComboBox()        
        imlec.execute("SELECT dalAdi FROM dal")
        dalListe = imlec.fetchall()
        dalUzunlugu = len(dalListe)        
        for i in range(0, dalUzunlugu):
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

        #---------VERİ TABANINA GİRİŞLER-------------------
        
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
                print(d)
                imlec = veritabani.cursor()                              
                #--------------------------------------------------
             
        
            sorgu = "INSERT INTO ogrenciBilgileri (ogrNo, ogrAd, ogrSoyad, subeSinif, telefon,egitimYili,veliAdSoyad,veliTelefon,adres,bolumID,dalID) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
           
            veri = [ogrNoText.text(),adText.text(),soyadText.text(),sinifSubeText.text(),telefonText.text(),comboYil.currentText(),adSoyadText.text(),telefonVeliText.text(),adresText.text(),int(b),int(d)]          
            imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
              
            #---------------VERİ TABANINA GİRİŞLER BİTİMİ----------------
            
            #---------------VERİ TABANI GÜNCELLEME BAŞLANGIÇ-------------
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
           
           #--------------------VERİ TABANI GÜNCELLEME BİTİŞ----------------
        
        
        
           #---------------------VERİ TABANI SİLME BAŞLANGIÇ-------------------------
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
        
           #--------------VERİ TABANI SİLME BİTİŞ----------------------
        
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
        
        
        veriOgrenciListesi = QTableWidget()
        #------VERİ TABANI TABLO GÖRÜNME BAŞLANGIÇ---------
        def yenile():
            veritabani = 'stajIsletme.sqlite'  
            veritabani = sqlite3.connect(veritabani)
            imlec = veritabani.cursor()              
            veriOgrenciListesi.setAlternatingRowColors(True)
            veriOgrenciListesi.setColumnCount(6)
            veriOgrenciListesi.horizontalHeader().setCascadingSectionResizes(False)
            veriOgrenciListesi.horizontalHeader().setSortIndicatorShown(False)
            veriOgrenciListesi.horizontalHeader().setStretchLastSection(True)
            veriOgrenciListesi.verticalHeader().setVisible(False)
            veriOgrenciListesi.verticalHeader().setCascadingSectionResizes(False)
            veriOgrenciListesi.verticalHeader().setStretchLastSection(False)
            veriOgrenciListesi.setHorizontalHeaderLabels(("Öğrenci No", "Öğrenci Adı","Öğrenci Soyad","Sınıfı","Bölümü","Dal"))
            veriOgrenciListesi.setMinimumSize(400,300)                    
            veriOgrenci = imlec.execute("SELECT ogrNo,ogrAd,ogrSoyad,o.subeSinif,bolumAdi,dalAdi FROM ogrenciBilgileri o,bolum b,dal d where b.bolumID=o.bolumID and d.dalID=o.dalID")
            veriOgrenci = veriOgrenci.fetchall()
            veriOgrenciListesi.setRowCount(0)
            for satirSayisi, satirVerisi in enumerate(veriOgrenci):
                veriOgrenciListesi.insertRow(satirSayisi)
                for sutunSayisi, sutunVeri in enumerate(satirVerisi):
                    print(sutunSayisi,sutunVeri)
                    veriOgrenciListesi.setItem(satirSayisi,sutunSayisi,QTableWidgetItem(str(sutunVeri)))
            veritabani.commit()
        
        #------VERİ TABANI TABLO GÖRÜNME BİTİŞ---------
        ogrenciListesiButonu=QPushButton('Öğrenci Listesi Yenile')
        ogrenciListesiButonu.setStyleSheet("background-color: #00ff6f; font-weight:bold")
        ogrenciListesiButonu.setGeometry(50, 50, 50, 50)
        ogrenciListesiButonu.clicked.connect(yenile)
        
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
        vbox2.addWidget(veriOgrenciListesi)
        vbox2.addWidget(ogrenciListesiButonu)
        
        
        gBoxVeli.setLayout(vbox2) 
        
        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxOgrenci) 
        mainLayout.addWidget(gBoxVeli) 
        
        vbox2.addStretch()
        
        self.setLayout(mainLayout)
        yenile()
        
class TabIsletme(QWidget):
    def __init__(self):
        super().__init__()
        gBoxIsletme= QGroupBox("İşletme Bilgileri")
        gBoxIsletme.setStyleSheet("font-weight:bold")
        gBoxIsletme.setMinimumSize(200,300)
        
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
        

        
       #------------isletmeBilgileri VERİ TABANINA GİRİŞLER-------------------
        
        def isletmeBilgiKayit():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()                             
                sorgu = "INSERT INTO isletmeBilgileri (isletmeAdi,temsilciAdSoyad,telefon,ePosta,vergiNo,sgkNo,adres,iban,tarihZaman,notu) VALUES(?,?,?,?,?,?,?,?,?,?)"                
                veri = [isletmeAdiText.text(),temsilciAdSoyadText.text(),telefonIsletmeText.text(),ePostaIsletmeText.text(),vergiNoText.text(),sgkNoText.text(),adresText.text(),ibanText.text(),egitimYiliIsletmeCombo.currentText(),notuText.text()]          
                imlec.execute(sorgu, veri)            
            veritabani.commit()
            veritabani.close()
                              
        #------------isletmeBilgileri VERİ TABANINA GİRİŞLER BİTİMİ---------------
                
        ekleButonu=QPushButton('İşletme Ekle') 
        ekleButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        ekleButonu.clicked.connect(isletmeBilgiKayit)
        
        isletmeSirasi = QLabel()
        isletmeSirasi.setText("İşletme Sırasını giriniz:")
        isletmeSirasiText=QLineEdit()
        
        isletmeSil=QPushButton('İşletme Sil')
        isletmeSil.setStyleSheet("background-color: #777; font-weight:bold")
        #-------------İŞLETME VERİ TABANI SİLME BAŞLANGIÇ--------------
        def isletmeBilgiSilme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                   
                sorgu = "DELETE FROM isletmeBilgileri where isletmeID=?"
                veri = [isletmeSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------İŞLETME VERİ TABANI SİLME BİTİŞ--------------
        isletmeSil.clicked.connect(isletmeBilgiSilme)
        isletmeGuncelle=QPushButton('İşletme Güncelle')
        isletmeGuncelle.setStyleSheet("background-color: #777; font-weight:bold")
         #-------------İŞLETME VERİ TABANI Güncelleme BAŞLANGIÇ--------------
        def isletmeBilgiGuncelleme():                                  
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor() 
                                  
                sorgu = "UPDATE isletmeBilgileri SET isletmeAdi=?,temsilciAdSoyad=?,telefon=?,\
                ePosta=?,vergiNo=?,sgkNo=?,adres=?,iban=?,tarihZaman=?,notu=? where isletmeID=?"
                veri = [isletmeAdiText.text(),temsilciAdSoyadText.text(),telefonIsletmeText.text(),\
                        ePostaIsletmeText.text(),vergiNoText.text(),sgkNoText.text(),adresText.text(),\
                        ibanText.text(),egitimYiliIsletmeCombo.currentText(),notuText.text(),isletmeSirasiText.text()] 
                imlec.execute(sorgu, veri)            
                veritabani.commit()
            veritabani.close()        
        
        #-------------İŞLETME VERİ TABANI Güncelleme BİTİŞ--------------
        isletmeGuncelle.clicked.connect(isletmeBilgiGuncelleme)
        
        gBoxsilmeGuncellemeIsletmeVeri= QGroupBox()
        silmeGuncellemeIsletmeH= QHBoxLayout()
        silmeGuncellemeIsletmeH.addWidget(isletmeSirasi)
        silmeGuncellemeIsletmeH.addWidget(isletmeSirasiText)
        gBoxsilmeGuncellemeIsletmeButon= QGroupBox()
        silmeGuncellemeIsletmeH2= QHBoxLayout()
        silmeGuncellemeIsletmeH2.addWidget(isletmeSil)
        silmeGuncellemeIsletmeH2.addWidget(isletmeGuncelle)
        
        
        
        
        gBoxIsletmeTablosu= QGroupBox("İşletme Bilgileri Listesi")
        gBoxIsletmeTablosu.setStyleSheet("font-weight:bold")
        
        veriIsletmeListesi = QTableWidget()
        #------VERİ TABANI TABLO GÖRÜNME BAŞLANGIÇ---------
        def yenile():
            veritabani = 'stajIsletme.sqlite'  
            veritabani = sqlite3.connect(veritabani)
            imlec = veritabani.cursor()              
            veriIsletmeListesi.setAlternatingRowColors(True)
            veriIsletmeListesi.setColumnCount(4)
            veriIsletmeListesi.horizontalHeader().setCascadingSectionResizes(False)
            veriIsletmeListesi.horizontalHeader().setSortIndicatorShown(False)
            veriIsletmeListesi.horizontalHeader().setStretchLastSection(True)
            veriIsletmeListesi.verticalHeader().setVisible(False)
            veriIsletmeListesi.verticalHeader().setCascadingSectionResizes(False)
            veriIsletmeListesi.verticalHeader().setStretchLastSection(False)
            veriIsletmeListesi.setHorizontalHeaderLabels(("İşletme Sırası", "İşletme Adı","Temsilci Ad Soyad","Telefon"))
            veriIsletmeListesi.setMinimumSize(400,300)                    
            veriIsletme = imlec.execute("SELECT isletmeID,isletmeAdi,temsilciAdSoyad,telefon FROM isletmeBilgileri")
            veriIsletme = veriIsletme.fetchall()
            veriIsletmeListesi.setRowCount(0)
            for satirSayisi, satirVerisi in enumerate(veriIsletme):
                veriIsletmeListesi.insertRow(satirSayisi)
                for sutunSayisi, sutunVeri in enumerate(satirVerisi):
                    print(sutunSayisi,sutunVeri)
                    veriIsletmeListesi.setItem(satirSayisi,sutunSayisi,QTableWidgetItem(str(sutunVeri)))
            veritabani.commit()
        
        #------VERİ TABANI TABLO GÖRÜNME BİTİŞ---------
        
        isletmeListesiButonu=QPushButton('İşletme Listesi Yenile')
        isletmeListesiButonu.setStyleSheet("background-color: #00ff6f; font-weight:bold")
        isletmeListesiButonu.setGeometry(50, 50, 50, 50)
        isletmeListesiButonu.clicked.connect(yenile)
                
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
        
        vbox1.addWidget(gBoxsilmeGuncellemeIsletmeVeri)
        gBoxsilmeGuncellemeIsletmeVeri.setLayout(silmeGuncellemeIsletmeH)
        vbox1.addWidget(gBoxsilmeGuncellemeIsletmeButon)
        gBoxsilmeGuncellemeIsletmeButon.setLayout(silmeGuncellemeIsletmeH2)
        gBoxIsletme.setLayout(vbox1)  
        
        vbox2 = QVBoxLayout()
        vbox2.addWidget(veriIsletmeListesi)
        vbox2.addWidget(isletmeListesiButonu)
        gBoxIsletmeTablosu.setLayout(vbox2)
        
        vbox1.addStretch()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(gBoxIsletme) 
        mainLayout.addWidget(gBoxIsletmeTablosu) 
        
        
        
        self.setLayout(mainLayout)
        yenile()
        
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
        
        
        kOgretmen = QLabel()
        kOgretmen.setText("Koordinatör Öğretmen")
        
        kAd = QLabel()
        kAd.setText("Ad")
        kAdText=QLineEdit()
        
        kSoyad = QLabel()
        kSoyad.setText("Soyad")
        kSoyadText=QLineEdit()

         #-----------VERİ TABANINA GİRİŞ--------
        
        def stajBilgiKayit():
            veritabani = 'stajIsletme.sqlite'
            dosya_var_mi = os.path.exists(veritabani)
            if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()
                #--------------------------------------------------
                veriAlmaIsletme="SELECT i.isletmeID FROM isletmeBilgileri as i where i.isletmeAdi=?"
                vIsletme=[comboIsletme.currentText()]
                imlec.execute(veriAlmaIsletme, vIsletme)
                isletmeAdiID = imlec.fetchone()
                iID=str(isletmeAdiID)
                i = iID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(i)
                veritabani.commit()
               #--------------------------------------------------
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[alanIsletmeText.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                veritabani.commit()
                #--------------------------------------------------
                veriAlmaDal="SELECT d.dalID FROM dal as d where d.dalAdi=?"
                vDal=[dalIsletmeText.currentText()]
                imlec.execute(veriAlmaDal, vDal)
                dalAdiID = imlec.fetchone()
                dID=str(dalAdiID)
                d = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b)
                veritabani.commit()
                
               
                
                #--------------------------------------------------
                veriAlmaOgrt="SELECT ogrtmenID FROM koordinatorOgretmen  where ogrtAd=? and ogrtSoyad=?"
                vk=[kAdText.text(),kSoyadText.text()]
                imlec.execute(veriAlmaOgrt, vk)
                kAdiID = imlec.fetchone()
                kID=str(kAdiID)
                k = iID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(k)
                veritabani.commit()
                #--------------------------------------------------
             
        
            sorgu = "INSERT INTO stajBilgileri (egitimYili,donem, isletmeID, bolumID,dalID,ogretmenID,tarihZaman) VALUES(?,?,?,?,?,?,?)"
           
            veri = [egitimYiliIsletmeCombo.currentText(),donemText.text(),int(i),int(b),int(d),int(k),egitimYiliIsletmeCombo.currentText()]          
            imlec.execute(sorgu, veri)            
            veritabani.commit()
           
        
            
        
        
        #--------VERİ TABANINA GİRİŞ BİTTİMİ----



        kaydetButonu=QPushButton('Kaydet') 
        kaydetButonu.setStyleSheet("background-color: #c71585; font-weight:bold")
        kaydetButonu.clicked.connect(stajBilgiKayit)
        
        
        
        
                
        vbox1 = QVBoxLayout()       
        vbox1.addWidget(isletmeAdi)
        vbox1.addWidget(comboIsletme)
        vbox1.addWidget(sinifSube)
        vbox1.addWidget(sinifSubeCombo)          
        vbox1.addWidget(alanIsletme)
        vbox1.addWidget(alanIsletmeText)  
        vbox1.addWidget(dalIsletme)
        vbox1.addWidget(dalIsletmeText)
        vbox1.addWidget(kOgretmen)
        vbox1.addWidget(kAd)
        vbox1.addWidget(kAdText)
        vbox1.addWidget(kSoyad)
        vbox1.addWidget(kSoyadText)
        
        vbox1.addWidget(egitimYiliIsletme)
        vbox1.addWidget(egitimYiliIsletmeCombo) 
        vbox1.addWidget(donem)
        vbox1.addWidget(donemText)
         
        
        vbox1.addWidget(kaydetButonu)
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
            adSoyadOgr = oAdSoyad.replace(",","").replace("[","").replace("]","").replace("'","").replace("(","").replace(")","\n")
            
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
        
        #----------VERİ TABANINDAN ALINMALI ALAN BİLGİLERİ---------------        
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
        
        #-----------İşletme Bilgileri Dosyaya Yazdırma--------------
        def isletmeBilgileriYazdir():
           veritabani = 'stajIsletme.sqlite'           
           dosya_var_mi = os.path.exists(veritabani)
           if dosya_var_mi:
                veritabani = sqlite3.connect(veritabani)
                imlec = veritabani.cursor()
                veriAlma="SELECT b.bolumID FROM bolum as b where b.bolumAdi=?"
                v=[comboAlan.currentText()]
                imlec.execute(veriAlma, v)
                bolumAdiID = imlec.fetchone()
                veritabani.commit()
                bID=str(bolumAdiID)
                b = bID.replace(",","").replace("(","").replace(")","").replace("'","")
                print(b) 
                              
           veriIsletme="SELECT i.isletmeID, i.isletmeAdi, i.temsilciAdSoyad, i.adres, i.telefon FROM  isletmeBilgileri i, stajBilgileri s,bolum b where b.bolumID=s.bolumID and i.isletmeID=s.isletmeID  "                               
          # veriGiris=[comboYil.currentText(),int(b)]
          # imlec.execute(veriIsletme, veriGiris)
           imlec.execute(veriIsletme)
           veri = imlec.fetchall()
           veritabani.commit()
           veriString=str(veri)
           veriDosya = veriString.replace(",","").replace("[","").replace("]","").replace("'","").replace("(","").replace(")","\n")
           if os.path.exists("isletmeBilgileri.txt"):
               with open("isletmeBilgileri.txt","w",encoding="utf-8") as dosya:
                   dosya.write(veriDosya)
        
        
        
        
        
        
        
        
        
        
        
        
        
        #----------------------------------------------
        isletmeListesiButonu=QPushButton('İşletme Listesi Al') 
        isletmeListesiButonu.setStyleSheet("background-color: #6e8b3d; font-weight:bold")
        isletmeListesiButonu.clicked.connect(isletmeBilgileriYazdir)
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
        
        


        
app = QApplication(sys.argv)
tabdialog = Tab()
tabdialog.show()
app.exec()
