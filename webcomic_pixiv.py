#! python3
#webcomic_pixiv.py: downloads images from pixiv posts. Currently doesn't work.

import requests, os, pyperclip, datetime
from bs4 import BeautifulSoup

url = pyperclip.paste()

try:
    identifier = url.split('/') #checks if the pasted material is splittable
    if 'pixiv' not in url or 'https://' not in url:
        print('The URL provided is not a pixiv link: ')
        exit()
    elif 'manga' not in url and 'medium' in url:
        print('The URL provided is a pixiv link, but the mode is incorrect. Make sure that the "See all" button is clicked. ')
        exit()
    elif 'mode' not in url:
        print('The URL provided is a Pixiv link, but this is not the correct post link.')
        exit()
except:
    print(url)
    print('Copy the complete Pixiv post link to the clipboard and try again.\n')
    exit()


page = requests.get(url)
page.raise_for_status()

soup = BeautifulSoup(page.text, 'lxml')
manga = soup.select('.manga')[0]
folderName = ((soup.find('title').text).split('」')[0]).split('「')[1]
folderPath = 'temp\\' + folderName
os.makedirs(folderPath, exist_ok='True')
print('Subfolder with path ' + folderPath + ' created.')
i = 0

illustID = url.split('=')[-1]

for img in manga.find_all('img'):
    imageName = img.get('data-src')
    imageFileName = os.path.basename(imageName)
    jpg = imageFileName.split('.')[-1]
    mangaPage = requests.get(imageName)
    i += 1
    print('Downloading image ' + imageFileName + ' as ' + str(i) + '.' + jpg + '...')
    imageFile = open(os.path.join(folderPath, str(i) + '.' + jpg), 'wb')
    for chunk in mangaPage.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    print(str(i) + '.' + jpg + ' downloaded.')

print('Done.\n')

artist = soup.find('a', class_ = 'user')
artistName = artist.text
artistPage = ('http://pixiv.net/' + artist.get('href')).format()


f = open(folderPath + '\\metadata.txt', 'w+')
f.write('Link: ' + url.format() + '\n')
f.write('Title: ' + folderName + '\n')
f.write('ID: ' + illustID + '\n')
f.write('Artist: ' + artistName + ' at ' + artistPage + '\n')
f.write(str(i) + ' images downloaded on datetime: ' + str(datetime.datetime.now()))

print('Metadata file created.\n')