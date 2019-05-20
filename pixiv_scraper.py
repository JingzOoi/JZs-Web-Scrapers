from requests_html import HTMLSession
import os
import timeit
from time import sleep

sess = HTMLSession()


class Album:
    def __init__(self, url):
        self.referer = url
        self.id = self.referer.split("=")[-1]
        self.name = self.id
        self.url = f'https://www.pixiv.net/ajax/illust/{self.id}/pages'
        self.page = sess.get(self.url)
        self.imageList = [item["urls"]["original"]
                          for item in self.page.json()["body"]]
        self.imageCount = len(self.imageList)
        self.valid = self.isValid()

    def isValid(self):
        if len(self.imageList) == 0:
            return False
        return True

    def download(self):
        dt = timeit.default_timer()

        destinationFolder = f'temp\\pixiv\\{self.id}'

        os.makedirs(destinationFolder, exist_ok=True)

        size = 0

        for num, link in enumerate(self.imageList, start=1):
            img = Image(link, referer=self.referer)
            img.download(destinationFolder=destinationFolder)
            size += img.size
            sleep(img.time)

        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'''
            Album URL: {self.url}
            Number of images: {len(self.imageList)}
            Total Size: {size:,} bytes
            ''')

        time = timeit.default_timer()-dt
        return time, size, self.imageCount


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
