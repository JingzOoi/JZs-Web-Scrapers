#! python3
# wcS_Twitter.py: Downloads image files off Twitter posts. 
#                 Supports images from 'main' post and 'reply' posts.
# Modules required: selenium, geckodriver (Firefox), requests, pyperclip
# Usage: [1] Copy the Twitter post link into the clipboard.
#        [2] Run the script. [In powershell (Windows) / terminal (Mac): python wcS_twitter.py)
#        [3] The images will be downloaded in the subfolder .\temp\<Twitter handle>\<post ID>.
#        [*] A metadata.txt file will be created to record the post and images info.
# Note: Now downloads :orig images as of 1 Jan 2019. 

from selenium import webdriver
import requests, os, pyperclip, datetime

# takes in url directly from clipboard
url = pyperclip.paste()

# validates url
try:
    # checks if url is splitable (i.e. not plain text)
    validation = url.split('/')

    # checks if url is a twitter link
    if 'https://twitter.com' not in url:
        print('URL is not a Twitter link.')
        exit()

    # checks if the link is splittable into 6 parts, as per a valid post link
    elif len(validation) != 6: 
        print('The URL provided is a Twitter link, but it is not a post link.')
        exit()
except:
    print('URL entered: {} \nCopy the correct link into the clipboard and try again.\n'.format(url))
    exit()

# creates folder based on Twitter handle and post ID in URL. Ignores if exists.
folderName = 'temp\\@{}\\{}'.format(url.split('/')[3], url.split('/')[-1])
os.makedirs(folderName, exist_ok = True)
print('Folder with name ' + folderName + ' created.')

# count
i = 0

# classes to be included in search
whitelist = ['permalink-in-reply-tos', 'permalink-tweet']

try:
    driver = webdriver.Firefox()
    driver.get(url)
    for class_ in whitelist:
        for post in driver.find_elements_by_class_name(class_):
            for container in post.find_elements_by_class_name('AdaptiveMediaOuterContainer'):
                for images in container.find_elements_by_tag_name('img'):
                    imageURL = images.get_attribute('src')
                    re = requests.get(imageURL + ':orig')
                    re.raise_for_status()
                    i += 1
                    
                    # defines image file names
                    imageName = os.path.basename(imageURL)
                    imageN = imageName.split('.')[1]
                    imageFileName = str(i) + "." + imageN

                    # downloads image files
                    print('Downloading image ' + imageName + " as " + imageFileName + "...")
                    imageFile = open(os.path.join(folderName, imageFileName), 'wb')      
                    for chunk in re.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
                    print('Image ' + imageName + ' downloaded.')
except:
    print('An error has occured. Check your connection and try again. \nIf this error persists, contact the developer to report this error.')
    exit()

print('Download tasks complete.\n')

# creates metadata.txt in folder
f = open(folderName + '\\metadata.txt', 'w+')
f.write('Link: ' + url + '\n')
f.write('Twitter handle: @' + url.split('/')[3] + '\n')
f.write('A total of {} images grabbed on datetime: {}\n'.format(str(i), str(datetime.datetime.now())))

print('Metadata file created. All operations complete.\n')

driver.close()