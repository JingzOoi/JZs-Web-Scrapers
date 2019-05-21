from requests_html import HTMLSession
import re
import os
import timeit
from time import sleep
from loadingBar import loadingBar

sess = HTMLSession()


class Album:
    def __init__(self, url):
        self.url = url
        self.page = sess.get(self.url)
        container = self.page.html.find('.tweet.permalink-tweet img')
        r = re.compile(r'https://pbs\.twimg\.com/media/([a-zA-z0-9-]+)\.jpg')
        self.imageList = [c.attrs["src"]
                          for c in container if re.match(r, c.attrs["src"])]
        self.imageCount = len(self.imageList)
        self.artist = self.url.split('/')[3]
        self.id = self.url.split('/')[5]
        self.name = self.id
        self.valid = self.isValid()

    def isValid(self):
        r = re.compile(r'https://twitter.com/[a-zA-Z_0-9]+/status/[0-9]+')
        if re.match(r, self.url) and self.imageCount > 0:
            return True
        return False

    def download(self):
        dt = timeit.default_timer()

        destinationFolder = f'temp\\twitter\\{self.artist}\\{self.name}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0

        for num, link in enumerate(self.imageList, start=1):
            img = Image(link)
            img.name = f'{num}{img.imageType}'
            img.download(destinationFolder=destinationFolder, name=img.name)
            loadingBar(len(self.imageList), num,
                       message=f'{num}/{len(self.imageList)} {img.name}')
            size += img.size
            sleep(img.time)

        print('\nDownloading operations complete.\nCreating metadata file.')

        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'''
            Album URL: {self.url}
            Number of images: {len(self.imageList)}
            Total Size: {size:,} bytes
            ''')

        time = timeit.default_timer()-dt

        print(
            f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, url):
        self.url = url
        self.image = sess.get(f'{self.url}:orig')
        self.size = int(self.image.headers["Content-Length"])
        self.name = os.path.basename(self.url)
        self.time = self.image.elapsed.total_seconds()
        self.imageType = os.path.splitext(self.name)[-1]

    def download(self, name, destinationFolder='temp\\twitter', ):
        with open(os.path.join(destinationFolder, name), 'wb') as img:
            img.write(self.image.content)
