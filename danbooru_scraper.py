from requests_html import HTMLSession
import os, loadingBar, timeit
from time import sleep

sess = HTMLSession()

class Collection:
    def __init__(self, pageURL):
        self.url = pageURL
        self.tag = pageURL.split('=')[-1]
        self.imageList = self.loop()
        self.imageCount = len(self.imageList)
        self.name = self.tag

    def loop(self, pageNum:int = 10):
        
        totalList = []
        
        for i in range(1, 1+pageNum):
            page = sess.get(f'https://danbooru.donmai.us/posts?page={i}&tags={self.tag}')
            tempList = [post.find("a", first=True).attrs["href"] for post in page.html.find('article.post-preview')]
            totalList.extend(tempList)

        return totalList

    def download(self, pageNum:int = 10):
        dt = timeit.default_timer()

        totalList = self.loop(pageNum)
        print(f'\n{len(totalList)} images found.')

        destinationFolder = f'temp\\danbooru\\{self.tag}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0
        typeCount = {
            'safe': 0,
            'questionable': 0,
            'explicit' : 0
        }
        
        for num, image in enumerate(totalList, start=1):
            try:
                img = Image(image)
                targetFolder = os.path.join(destinationFolder, img.rating)
                os.makedirs(targetFolder, exist_ok=True)
                with open(os.path.join(targetFolder, f'[{num}] - {img.name}'), 'wb') as file:
                    file.write(img.image.content)

                size += img.size

                typeCount[f'{img.rating}'] += 1

                loadingBar.loadingBar(len(totalList), num, message=f'{num}/{len(totalList)} ..{img.name[:18]}')
                sleep(img.time)
            except:
                continue

        print('\nDownloading operations complete.\nCreating metadata file.')
        
        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'''
            Album URL: {self.url}
            Tag: {self.tag}
            Number of images: {len(totalList)}
            Total Size: {size:,} bytes
            Status: {typeCount}
            ''')

        time = timeit.default_timer()-dt
        
        print(f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')



class Image:
    def __init__(self, imagePageURL):
        self.url = f'https://danbooru.donmai.us{imagePageURL}'
        self.page = sess.get(self.url)
        self.links = self.page.html.find('section#post-information ul li a')
        self.link = self.links[-2].attrs["href"]
        self.source = self.links[-1].attrs["href"]
        self.rating = self.page.html.find('section#post-information ul li')[-4].text.split(':')[-1].strip().lower()
        self.image = sess.get(self.link)
        self.size = int(self.image.headers["Content-Length"])
        if 'pixiv' in self.source and 'fanbox' not in self.source:
            self.sourceID = self.source.split('=')[-1]
            self.sourceSite = 'pixiv'
        elif 'twitter' in self.source:
            self.sourceID = f'@{self.source.split("/")[3]}_{self.source.split("/")[5]}'
            self.sourceSite = 'twitter'
        else:
            self.sourceID = '-----none'
            self.sourceSite = 'other-----'

        self.imageType = os.path.splitext(self.link)[-1]

        self.name = f'{self.sourceSite}_{self.sourceID}{self.imageType}'
        self.time = self.image.elapsed.total_seconds()
        