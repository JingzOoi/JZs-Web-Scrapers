#! python3
#webcomic_twitter.py: Downloads image files from Twitter posts. Max 4 images per post because Twitter.
#usage: [1] Copy the twitter link into your clipboard.
#       [2] Run the script. (Through powershell/cmd/terminal: python webcomic_twitter.py)
#       [3] The image files will be saved into \temp\<postID> of the same folder.
#modules required: bs4, requests, os, pyperclip
#note: does not support images in replies as of 30 Dec 2018, only images from the 'main' post.

from bs4 import BeautifulSoup
import requests, os
from pyperclip import paste
import datetime

#pastes from clipboard
url = paste()
print(url)

#tests if the pasted content: [1] is a link [2] is a Twitter link
try:
    identifier = url.split('/')[2]
    if 'twitter' not in url or 'https://' not in url:
        print('The URL provided is not a Twitter link.\n')
        exit()
except:
    print('Copy the complete Twitter link onto the clipboard and try again.')
    exit()

#gets twitter page
page = requests.get(url)
r = page.raise_for_status()

soup = BeautifulSoup(page.text, 'lxml')
#specifies container if images exist in post
try:
    container = soup.select('.AdaptiveMediaOuterContainer')[0]
except IndexError:
    print('\nImage files not found. Please confirm that the Twitter post contain images to be fetched.')
    print('Last item on clipboard: ' + url + '\n')
    exit()

#creates subfolder with the postID
folderName = 'temp\\' + url.split('/')[-1] + ' (Twitter)'
os.makedirs(folderName, exist_ok = True)
print('Subfolder with name ' + folderName + ' created.')
i = 0

#selects and downloads images
for images in container.find_all('img'):
    imageURL = images.get('src')
    re = requests.get(imageURL)
    re.raise_for_status()
    i += 1

    imageName = os.path.basename(imageURL)
    imageN = imageName.split('.')[1]
    imageFileName = str(i) + "." + imageN
    print('Downloading image ' + imageName + " as " + imageFileName + "...")
    imageFile = open(os.path.join(folderName, imageFileName), 'wb')

    for chunk in re.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    print('Image ' + imageName + ' downloaded.')

print('Done.\n')

f = open(folderName + '\\metadata.txt', 'w+')
f.write('Link: ' + url.format() + '\n')
f.write('Twitter handle: @' + url.split('/')[3] + '\n')
f.write(str(i) + ' images grabbed on datetime: ' + str(datetime.datetime.now()) + '\n')

print('Metadata file created.\n')