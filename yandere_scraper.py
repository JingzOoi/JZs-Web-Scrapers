from requests_html import HTMLSession
import os
from loadingBar import loadingBar
import timeit
from time import sleep
import re

sess = HTMLSession()


class Collection:
    def __init__(self, url):
        self.url = url
        self.tag = self.url.split('=')[-1]
        self.name = self.tag
        self.valid = self.verifyTag()

    def verifyTag(self):
        page = sess.get(self.url)
        p = page.html.find('.content div p', first=True)
        if p is None:
            return True
        elif 'Nobody here but us chickens!' in p.text:
            return False
        return True

    def loop(self, pageNum: int = 10):

        totalList = []

        for i in range(1, 1+pageNum):
            page = sess.get(f'https://yande.re/post?page={i}&tags={self.tag}')
            tempList = [post.attrs["href"]
                        for post in page.html.find('ul#post-list-posts li div a.thumb')]
            totalList.extend(tempList)

        return totalList

    def download(self, pageNum: int = 10):
        dt = timeit.default_timer()

        totalList = self.loop(pageNum)
        print(f'\n{len(totalList)} images found.')

        destinationFolder = f'temp\\yandere\\{self.tag}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0
        typeCount = {}

        for num, image in enumerate(totalList, start=1):
            try:
                img = Image(image)
                targetFolder = os.path.join(destinationFolder, img.rating)
                os.makedirs(targetFolder, exist_ok=True)

                img.download(num, targetFolder)

                size += img.size

                if img.rating not in typeCount.keys():
                    typeCount[f'{img.rating}'] = 1
                else:
                    typeCount[f'{img.rating}'] += 1

                loadingBar(len(totalList), num,
                           message=f'{num}/{len(totalList)} {img.name}')

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

        print(
            f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, imagePageURL):
        self.url = f'https://yande.re{imagePageURL}'
        self.page = sess.get(self.url)
        self.sidebar = self.page.html.find('.sidebar div ul')
        self.tags = self.sidebar[0]

        self.stats = self.sidebar[1].text.split()
        self.id = self.stats[self.stats.index('Id:')+1]
        self.rating = self.stats[self.stats.index('Rating:')+1]

        self.options = self.sidebar[2]
        try:
            self.link = self.options.find(
                '.original-file-unchanged', first=True).attrs["href"]
        except AttributeError:
            self.link = self.options.find(
                '.original-file-changed')[-1].attrs["href"]
        self.image = sess.get(self.link)
        self.size = int(self.image.headers["Content-Length"])
        self.imageType = os.path.splitext(self.link)[-1]
        self.name = f'yande.re - {self.id}{self.imageType}'
        self.time = self.image.elapsed.total_seconds()

    def download(self, num: int = 0, destinationFolder='temp\\yandere'):
        with open(os.path.join(destinationFolder, f'[{num}] - {self.name}'), 'wb') as img:
            img.write(self.image.content)
