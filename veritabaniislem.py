import os
import sqlite3 as sql
from lxml import html
import requests
class Veritabani:
    def __init__(self):
        self.page = requests.get('http://www.nkariyer.com/egitim/2019/10/23/meslek-lisesi-bolumleri-nelerdir-meslek-lisesinde-hangi-bolumler-var-iste-meslek-liselerinde-yer-alan-bolumler-ve-dallarinin-tam-listesi')
        self.tree = html.fromstring(self.page.content)
        self.dosyaismi="staj.sqlite"
        self.dosya_var_mi= os.path.exists(self.dosyaismi)
        if self.dosya_var_mi==True:    
            self.vt =sql.connect("staj.sqlite")
            self.imlec=self.vt.cursor()
        self.veritabaniTabloOlustur()
        
    def veritabaniTabloOlustur(self):        
        self.imlec.execute("CREATE TABLE IF NOT EXISTS ogrencibilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT, ogrNo,ad,soyad,subeSinif,telefon,veliAdSoyad,veliTelefon,adres,il,bolumid,dalid )")
        self.imlec.execute("CREATE TABLE IF NOT EXISTS isletmebilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT,isletmeAdi,temsilciAdSoyad,telefon,eposta,vergiNo,SGKNo,adres,il,iban,tarihZaman,notu )")          
        self.imlec.execute("CREATE TABLE IF NOT EXISTS stajbilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT, egitimYili,donem,isletmeId,bolumId,dalId,ogretmenId,OgrNo,tarihZaman)")
        self.imlec.execute("CREATE TABLE IF NOT EXISTS koordinatorogretmentbl(id INTEGER PRIMARY KEY AUTOINCREMENT, ad,soyad,bolumid)")    
        self.imlec.execute("CREATE TABLE IF NOT EXISTS bolumtbl(id INTEGER PRIMARY KEY AUTOINCREMENT, bolumadi )")
        self.imlec.execute("CREATE TABLE IF NOT EXISTS daltbl(id INTEGER PRIMARY KEY AUTOINCREMENT, daladi )")
        self.imlec.execute("CREATE TABLE IF NOT EXISTS iltbl(id INTEGER PRIMARY KEY AUTOINCREMENT, iladi )")
        self.illerikaydet()
            
    def illerikaydet(self):
        iller = ["istanbul", "ankara", "izmir", "adana", "adıyaman", "afyonkarahisar", "ağrı", "aksaray", "amasya",
                    "antalya", "ardahan", "artvin", "aydın", "balıkesir", "bartın", "batman", "bayburt", "bilecik", "bingöl",
                    "bitlis", "bolu", "burdur", "bursa", "çanakkale", "çankırı", "çorum", "denizli", "diyarbakır", "düzce", "edirne",
                    "elazığ", "erzincan", "erzurum", "eskişehir", "gaziantep", "giresun", "gümüşhane", "hakkari", "hatay", "ığdır",
                    "ısparta", "kahramanmaraş", "karabük", "karaman", "kars", "kastamonu", "kayseri", "kırıkkale", "kırklareli",
                    "kırşehir", "kilis", "kocaeli", "konya", "kütahya", "malatya", "manisa", "mardin", "mersin", "muğla", "muş",
                    "nevşehir", "niğde", "ordu", "osmaniye", "rize", "sakarya", "samsun", "siirt", "sinop", "sivas", "şırnak",
                    "tekirdağ", "tokat", "trabzon", "tunceli", "şanlıurfa", "uşak", "van", "yalova", "yozgat", "zonguldak"]
        for x in iller:       
            sorgu = "INSERT INTO iltbl (iladi) VALUES (?)"
            veri=[x]
            self.imlec.execute(sorgu,veri)
        self.bolumlerikaydet()
        
    def bolumlerikaydet(self):
        bolumler=self.tree.xpath('//h3/strong/text()')
        bolumler.pop(0)
        for y in bolumler:
            k=str(y)
            bosluk=k.index(" ")
            bolum=k[bosluk:]
            sorgu = "INSERT INTO bolumtbl (bolumadi) VALUES (?)"
            veri=[bolum]
            self.imlec.execute(sorgu,veri)
        self.alanlarikaydet()
        
    def alanlarikaydet(self):
        dallar=self.tree.xpath('//p/text()')
        dallar.pop(len(dallar)-1)
        dallar.pop(len(dallar)-1)
        dallar.pop(0)
        for x in dallar:
            z=str(x)
            bos=z.index(" ")
            dal=z[bos:]
            sorgu = "INSERT INTO daltbl (daladi) VALUES (?)"
            veri=[dal]
            self.imlec.execute(sorgu,veri)
        self.vt.commit()
        #self.vt.close()
        
    def bolumgetir(self):
        self.imlec.execute("SELECT * FROM bolumtbl")
        bolumler= self.imlec.fetchall()
        return bolumler
    
    def dalgetir(self):
        self.imlec.execute("SELECT * FROM daltbl")
        dallar= self.imlec.fetchall()
        return dallar
    def ilgetir(self):
        self.imlec.execute("SELECT * FROM iltbl")
        iller= self.imlec.fetchall()
        return iller
        
        
            
Veritabani()
print(Veritabani().bolumgetir())
print(Veritabani().dalgetir())
print(Veritabani().ilgetir())
