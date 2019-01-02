#! python3
# wcS_Twitter.py: Downloads image files off Twitter posts. 
#                 Supports images from 'main' post and 'reply' posts.
# Usage: [1] Copy the Twitter post link into the clipboard.
#        [2] Run the script. [In powershell (Windows) / terminal (Mac): python webcomic_twitter.py <url>]
#        [3] The images will be downloaded in the subfolder .\temp\<Twitter handle>\<post ID>.
#        [*] A metadata.txt file will be created to record the post and images info.
# Note: Now downloads :orig images as of 1 Jan 2019. 

# Additional modules required: requests, bs4, scraperFunctions

from bs4 import BeautifulSoup
import requests, os, sys, scraperFunctions

# takes URL from first argument
url = sys.argv[1]
sess = requests.Session()
# validates url
try:
    scraperFunctions.validateURL(url, 'https://twitter.com', 6)
except:
    print('URL entered: {} \nCopy the correct link into the clipboard and try again.\n'.format(url))
    exit()

folder1 = url.split('/')[3]
folder2 = url.split('/')[-1]
folderName = scraperFunctions.createFolderPath(folder1, folder2)

# count
i = 0

# limits the type of division from which the images are taken
whitelist = ['permalink-in-reply-tos', 'permalink-tweet']

try:
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'lxml')

    for wl in whitelist: 
        for post in soup.find_all('div', class_ = wl):
            for container in post.select('.AdaptiveMediaOuterContainer'):
                for images in container.find_all('img'):

                    # gets the image link, tries to get the original image file (:orig) instead of the shrinked version shown
                    imageURL = images.get('src')
                    re = sess.get(imageURL + ':orig')
                    re.raise_for_status()
                    i += 1

                    imageRenaming = scraperFunctions.imageRename(imageURL, i)
                    imageNName = imageRenaming[0]
                    imageOName = imageRenaming[1]

                    scraperFunctions.imageDownload(re, folderName, imageOName, imageNName)
except:
    print('An error has occured. Check your connection and try again. \nIf this error persists, contact the developer to report this error.')
    exit()

print('Download tasks complete. Creating metadata file.\n')

authorName = url.split('/')[3]
scraperFunctions.createMetadata(folderName, authorName, url, i)

print('Metadata file created. All operations complete.\n')