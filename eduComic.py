#! python3
# eduComic.py: Downloads educational comics from the website nhentai.net.
# Usage: [1] Run the script. (python eduComic.py)
#        [2] When prompted, enter the magical 6-digit number.
# Additional modules: requests, bs4

import requests, os, datetime
from bs4 import BeautifulSoup

number = input('Enter the magical 6-digit number: ')
sess = requests.Session()

try:
    # checks if url is splitable (i.e. not plain text)
    if len(number) != 6:
        print('The input was not the magical number.')
        exit()
    else:
        url = 'https://nhentai.net/g/' + number

    print('Getting gallery information...')
    page = sess.get(url)
    page.raise_for_status()
    
    soup = BeautifulSoup(page.text, 'lxml')

    for tag in soup.find_all('a', class_ = 'tag'):
        if '/artist/' in tag.get('href'):
            authorName = tag.get('href').split('/')[-2]


    folderName = 'temp\\eduComic\\{}\\{}'.format(authorName, number)
    os.makedirs(folderName, exist_ok = True)
    print('Folder with name ' + folderName + ' created. \nStarting download operations.')

    i = 0
    galleryLen = len(soup.select('.gallerythumb'))
    for thumb in soup.select('.gallerythumb'):
        i += 1
        pageURL = 'https://nhentai.net' + thumb.get('href')
        pagePage = sess.get(pageURL)
        pageSoup = BeautifulSoup(pagePage.text, 'lxml')
        imageURL = pageSoup.select('img')[1].get('src')
        
        imageName = os.path.basename(imageURL)
        load = '[{}/{}] Downloading image '.format(str(i).rjust(len(str(galleryLen))), galleryLen) + imageName + '...'
        print(load, end='')
        
        re = sess.get(imageURL)
        with open(os.path.join(folderName, imageName), 'wb') as imageFile:   
            imageFile.write(re.content)
        imageFile.close()
        print('\b'*len(load), end='', flush=True)

    print('\nDownload operations complete. {} images has been downloaded. \nCreating metadata file.\n'.format(str(i)))

    f = open(folderName + '\\metadata.txt', 'w+')
    f.write('Link: ' + url + '\n')
    f.write('Created by: ' + authorName + '\n')
    f.write('A total of {} image(s) grabbed on datetime: {}\n'.format(str(i), str(datetime.datetime.now())))

    print('All operations complete.\n')
except:
    print('Please check your network connection and try again.')
    exit()