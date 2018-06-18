import time
import os
from bs4 import BeautifulSoup
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class Car():
    def __init__(self,nom="",prix="",link=""):
        self.nom = nom
        self.prix = prix
        self.link = link

Cars = []

url = "https://www.leboncoin.fr/voitures/offres/rhone_alpes/?th=1&w=4&latitude=45.39146&longitude=4.26846&radius=100000&ps=10&pe=14&me=70000"

while(True):
    NewCars = []
    html = urllib.request.urlopen(url,context=ctx)
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.findAll('li',itemtype="http://schema.org/Offer"):
        title = item.find('h2').string
        prix = item.find('h3').string
        link = item.find('a').get('href')[2:]
        try:
            img = item.find('span').find('span').get('data-imgsrc')
            os.system('wget "'+img+'"')
        except:
            img = ''
        if Cars == [] or title != Cars[0].nom:
            NewCars.append(Car(nom=title,prix=prix,link=link))
            fichier = open("data.txt", "a")
            fichier.write(title+'\n')
            fichier.write(prix+'\n')
            fichier.write(link+'\n\n')
            fichier.write('----------------------------------------------------------------------------- \n\n')
            fichier.close()
            file = img[35:]
            os.system('notify-send -i $PWD/"'+file+'" "'+title+'" "'+prix+'"')
        else:
            break

    Cars = NewCars+Cars

    time.sleep(360)
