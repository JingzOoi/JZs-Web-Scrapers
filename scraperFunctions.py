# to fix: too many positional arguments?
# Created: 2 Jan 2019

import datetime, os

def validateURL(url, website, length):
    # checks if url is splitable (i.e. not plain text)
    validation = url.split('/')

    # checks if url is a twitter link
    if website not in url:
        print('URL is not a {} link.'.format(website))
        exit()

    # checks if the link is splittable into 6 parts, as per a valid post link
    elif len(validation) != length: 
        print('The URL provided is a {} link, but not a post link.'.format(website))
        exit()

# creates folder based on Twitter handle and post ID in URL. Ignores if exists.
def createFolderPath(folder1, folder2):
    folderName = 'temp\\@{}\\{}'.format(folder1, folder2)
    os.makedirs(folderName, exist_ok = True)
    print('Folder with name ' + folderName + ' created.')
    return folderName

# attaches original file extension to new image name
def imageRename(imageURL, i):
    imageOName = os.path.basename(imageURL)
    imageExtension = imageOName.split('.')[-1]
    imageNName = str(i) + "." + imageExtension
    return imageNName, imageOName


# downloads image files to created folder
def imageDownload(re, folderName, imageOName, imageNName):
    print('Downloading image ' + imageOName + " as " + imageNName + "...")
    with open(os.path.join(folderName, imageNName), 'wb') as imageFile:   
        imageFile.write(re.content)
    imageFile.close()
    print('Image ' + imageOName + ' downloaded.')

# creates metadata.txt in folder
def createMetadata(folderName, authorName, url, i):
    f = open(folderName + '\\metadata.txt', 'w+')
    f.write('Link: ' + url + '\n')
    f.write('Twitter handle: @' + authorName + '\n')
    f.write('A total of {} image(s) grabbed on datetime: {}\n'.format(str(i), str(datetime.datetime.now())))