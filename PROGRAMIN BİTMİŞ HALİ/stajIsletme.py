# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 12:03:53 2020

@author: Şermin
"""

import sqlite3
import sys
import os
from PyQt5.QtWidgets import QApplication

def veriTabaniOlustur():

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
if __name__ == '__main__':
   app = QApplication(sys.argv)
   veriTabaniOlustur()
   app.exec()