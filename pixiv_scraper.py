from requests_html import HTMLSession
import os
import timeit
from time import sleep
from loadingBar import loadingBar

sess = HTMLSession()


class Album:
    def __init__(self, url):
        self.referer = url
        self.id = self.referer.split("=")[-1]
        self.name = self.id
        self.url = f'https://www.pixiv.net/ajax/illust/{self.id}/pages'
        self.page = sess.get(self.url, headers={'referer': self.referer})
        self.imageList = [item["urls"]["original"]
                          for item in self.page.json()["body"]]
        self.imageCount = len(self.imageList)
        self.valid = self.isValid()
        if self.page.json()['error'] == True:
            raise Exception('ID does not exist, or the album is r18.')

    def __repr__(self):
        return f'{self.referer}\n{self.url}\n{self.imageList}'

    def isValid(self):
        if len(self.imageList) == 0:
            return False
        return True

    def download(self):
        dt = timeit.default_timer()

        destinationFolder = f'temp\\pixiv\\{self.id}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0

        for num, link in enumerate(self.imageList, start=1):
            img = Image(link, referer=self.referer)
            img.download(destinationFolder=destinationFolder)
            loadingBar(len(self.imageList), num,
                       message=f'{num}/{len(self.imageList)} {img.name}')
            size += img.size
            sleep(img.time)

        print('\nDownloading operations complete.\nCreating metadata file.')

        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'''
            Album URL: {self.referer}
            Number of images: {len(self.imageList)}
            Total Size: {size:,} bytes
            ''')

        time = timeit.default_timer()-dt

        print(
            f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, url, referer):
        self.url = url
        self.referer = referer
        self.image = sess.get(self.url, headers={'referer': url})
        self.size = int(self.image.headers["Content-Length"])
        self.name = os.path.basename(url)
        self.time = self.image.elapsed.total_seconds()

    def download(self, destinationFolder='temp\\pixiv'):
        with open(os.path.join(destinationFolder, self.name), 'wb') as img:
            img.write(self.image.content)
