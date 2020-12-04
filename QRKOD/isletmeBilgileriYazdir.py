# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:33:47 2020

@author: Şermin
"""

# Paketleri yükle
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

pdfmetrics.registerFont(TTFont('Montserrat-Bold',"fonts\\Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont('Montserrat-Regular',"fonts\\Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont('Montserrat-Light',"fonts\\Montserrat-Light.ttf"))
pdfmetrics.registerFont(TTFont('Montserrat-LightItalic',"fonts\\Montserrat-LightItalic.ttf"))
pdfmetrics.registerFont(TTFont('Montserrat-Black',"fonts\\Montserrat-Black.ttf"))


# Excel dosyasını al
isletme_listesi = pd.read_excel('isletme_listesi.xlsx', sheet_name='isletme_listesi')

isletme_listesi
# PDF ayarla
packet = io.BytesIO()

kart_boyutu = (3.54, 5.31)
kanvas = canvas.Canvas(packet, pagesize=kart_boyutu)

for index, row in isletme_listesi.iterrows():
    no, isletmeAdi, adres, ilce, ili = row['No'], row['businessName'],row['Adress'],row['District'],row['City']
    print(no, isletmeAdi, adres, ilce, ili)
    
    
    
    # QR Code Kısmı
    
    qr = qrcode.QRCode(version=1, box_size=1.5, border=2)
    qr.add_data("{} {} {} {} {}".format( no, isletmeAdi, adres, ilce, ili))
    qr.make(fit=True)
    img = qr.make_image(image_factory= qrcode.image.pil.PilImage, fill_color='black', back_color='white')
    img = img.resize((64,64), Image.ANTIALIAS)
    img.save('qrcode{}.png'.format(no))
    kanvas.drawImage('qrcode{}.png'.format(no),1.3*inch,1.3*inch)
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




