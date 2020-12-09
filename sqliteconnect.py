import os
import sqlite3 as sql
from lxml import html
import requests

page = requests.get('http://www.nkariyer.com/egitim/2019/10/23/meslek-lisesi-bolumleri-nelerdir-meslek-lisesinde-hangi-bolumler-var-iste-meslek-liselerinde-yer-alan-bolumler-ve-dallarinin-tam-listesi')
tree = html.fromstring(page.content)
dosyaismi="staj.sqlite"
dosya_var_mi= os.path.exists(dosyaismi)
if dosya_var_mi==False:    
    vt =sql.connect("staj.sqlite")
    imlec=vt.cursor()
    
    imlec.execute("CREATE TABLE IF NOT EXISTS ogrencibilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT, ogrNo,ad,soyad,subeSinif,telefon,veliAdSoyad,veliTelefon,adres,il,bolumid,dalid )")
    imlec.execute("CREATE TABLE IF NOT EXISTS isletmebilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT,isletmeAdi,temsilciAdSoyad,telefon,eposta,vergiNo,SGKNo,adres,il,iban,tarihZaman,notu )")          
    imlec.execute("CREATE TABLE IF NOT EXISTS stajbilgileritbl(id INTEGER PRIMARY KEY AUTOINCREMENT, egitimYili,donem,isletmeId,bolumId,dalId,ogretmenId,OgrNo,tarihZaman)")
    imlec.execute("CREATE TABLE IF NOT EXISTS koordinatorogretmentbl(id INTEGER PRIMARY KEY AUTOINCREMENT, ad,soyad,bolumid)")
    
    imlec.execute("CREATE TABLE IF NOT EXISTS bolumtbl(id INTEGER PRIMARY KEY AUTOINCREMENT, bolumadi )")
    bolumler=tree.xpath('//h3/strong/text()')
    bolumler.pop(0)
    for y in bolumler:
        k=str(y)
        bosluk=k.index(" ")
        bolum=k[bosluk:]
        sorgu = "INSERT INTO bolumtbl (bolumadi) VALUES (?)"
        veri=[bolum]
        imlec.execute(sorgu,veri)
        
    imlec.execute("CREATE TABLE IF NOT EXISTS daltbl(id INTEGER PRIMARY KEY AUTOINCREMENT, daladi )")
    dallar=tree.xpath('//p/text()')
    dallar.pop(len(dallar)-1)
    dallar.pop(len(dallar)-1)
    dallar.pop(0)
    for x in dallar:
        z=str(x)
        bos=z.index(" ")
        dal=z[bos:]
        sorgu = "INSERT INTO daltbl (daladi) VALUES (?)"
        veri=[dal]
        imlec.execute(sorgu,veri)
        
    imlec.execute("CREATE TABLE IF NOT EXISTS iltbl(id INTEGER PRIMARY KEY AUTOINCREMENT, iladi )")
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
        imlec.execute(sorgu,veri)     
    
    imlec.execute("SELECT * FROM bolumtbl")
    bolumler= imlec.fetchall()
    print(bolumler) 
    
    imlec.execute("SELECT * FROM daltbl")
    daltbl= imlec.fetchall()
    print(daltbl)
    
    imlec.execute("SELECT * FROM iltbl")
    iltbl= imlec.fetchall()
    print(iltbl)  
        
    vt.commit()
    vt.close()