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
        self.imageList = self.loop()
        self.imageCount = len(self.imageList)
        self.name = self.tag

    def loop(self, pageNum: int = 10):

        totalList = []

        for i in range(1, 1+pageNum):
            page = sess.get(
                f'https://danbooru.donmai.us/posts?page={i}&tags={self.tag}')
            tempList = [post.attrs["href"]
                        for post in page.html.find('#posts-container article a')]
            totalList.extend(tempList)

        return totalList

    def download(self, pageNum: int = 10):
        dt = timeit.default_timer()

        totalList = self.loop(pageNum)
        print(f'\n{len(totalList)} images found.')

        destinationFolder = f'temp\\danbooru\\{self.tag}'
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

            except ConnectionError:
                break
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
        self.url = f'https://danbooru.donmai.us{imagePageURL}'
        self.page = sess.get(self.url)

        self.info = self.page.html.find('section#post-information', first=True)
        self.info_text = self.info.text.split()

        self.id = self.info_text[self.info_text.index('ID:')+1]
        self.rating = self.info_text[self.info_text.index('Rating:')+1]
        for a in self.info.links:
            r = re.compile(
                r'https://(danbooru|raikou2)\.donmai\.us/([A-Za-z0-9_/+]+)\.([a-z]{3,4})')
            x = re.search(r, a)
            if x:
                self.link = x.group()
                break
            else:
                raise Exception(f'Matching link not found in {self.url}')

        self.image = sess.get(self.link)
        self.size = int(self.image.headers["Content-Length"])
        self.imageType = os.path.splitext(self.link)[-1]
        self.name = f'danbooru - {self.id}{self.imageType}'
        self.time = self.image.elapsed.total_seconds()

    def download(self, num: int = 0, destinationFolder='temp\\danbooru'):
        with open(os.path.join(destinationFolder, f'[{num}] - {self.name}'), 'wb') as img:
            img.write(self.image.content)
