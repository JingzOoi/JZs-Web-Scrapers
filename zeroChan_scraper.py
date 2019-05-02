from requests_html import HTMLSession
import os, loadingBar, timeit
from time import sleep

sess = HTMLSession()

class Collection:
    def __init__(self, tagMainURL):
        self.url = tagMainURL
        self.imageList = self.loop()
        self.imageCount = len(self.imageList)
        self.tag = self.url.split('/')[-1].replace('+',' ')
        self.name = self.tag

    def loop(self, pageNum:int = 10):
        
        totalList = []
        
        for i in range(1, 1+pageNum):
            page = sess.get(f'{self.url}?p={i}')
            tempList = [f'https://zerochan.net{image.find("a", first=True).attrs["href"]}' for image in page.html.find('#thumbs2 li') if 'register' not in image.find('a', first=True).attrs["href"]]
            totalList.extend(tempList)

        return totalList

    def download(self, pageNum:int = 10):

        dt = timeit.default_timer()

        totalList = self.loop(pageNum)
        print(f'\n{len(totalList)} images found.')

        destinationFolder = f'temp\\zeroChan\\{self.tag}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0

        for num, image in enumerate(totalList, start=1):

            img = Image(image)

            with open(os.path.join(destinationFolder, f'[{num}] - {img.name}'), 'wb') as file:
                file.write(img.image.content)

            size += img.size

            loadingBar.loadingBar(len(totalList), num, message=f'{num}/{len(totalList)} {img.name}')
            sleep(img.time)

        print('\nDownloading operations complete.\nCreating metadata file.')
        
        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'Album URL: {self.url}\nTag: {self.tag}\nNumber of images: {len(totalList)}\nTotal Size: {size:,} bytes')

        time = timeit.default_timer()-dt
        
        print(f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')
            
    
class Image:
    def __init__(self, imagePageURL):
        self.url = imagePageURL
        self.page = sess.get(self.url)
        self.id = self.url.split('/')[-1]
        try:
            self.link = self.page.html.find('.preview', first=True).attrs["href"]
        except:
            self.link = self.page.html.find('#large img', first=True).attrs["src"]
        self.image = sess.get(self.link)
        self.name = f'{self.id}.{os.path.basename(self.link).split(".")[-1]}'
        self.size = int(self.image.headers["Content-Length"])
        self.time = self.image.elapsed.total_seconds()