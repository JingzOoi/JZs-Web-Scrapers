from requests_html import HTMLSession
import os
import timeit
from time import sleep
from loadingBar import loadingBar
import re
from pixiv_compilation import compile_artist
import random
import string

sess = HTMLSession()


class Album:
    def __init__(self, url):
        self.referer = url
        self.id = self.referer.split("=")[-1]
        self.name = self.id
        try:
            self.url = f'https://www.pixiv.net/ajax/illust/{self.id}/pages'
            self.page = sess.get(self.url, headers={
                                 'referer': self.referer, 'x-user-id': '23245428'})
        except ConnectionError:
            raise Exception(
                'Connection severed. Might have been rate limited.')

        self.imageList = [item["urls"]["original"]
                          for item in self.page.json()["body"]]
        self.imageCount = len(self.imageList)
        self.valid = self.isValid()
        if self.page.json()['error'] == True:
            raise Exception('ID does not exist, or the album is r18.')
        self.detail = sess.get(
            f'https://www.pixiv.net/ajax/user/{random.randint(1000000, 9999999)}/illusts?ids[]={self.id}').json()
        if self.detail["error"] == True:
            raise Exception("An error has occured. Try again.")
        else:
            self.detailBody = self.detail["body"]
            self.title = self.detailBody[f"{self.id}"]["illustTitle"]
            self.artist = self.detailBody[f"{self.id}"]["userName"]
            self.artistID = self.detailBody[f"{self.id}"]["userId"]
            self.tags = self.detailBody[f"{self.id}"]["tags"]

    def __repr__(self):
        return f'{self.referer}\n{self.url}\n{self.imageList}'

    def isValid(self):
        r = re.compile(
            r'https://www\.pixiv\.net/member_illust\.php\?mode=medium&illust_id=([0-9]+)')
        if re.match(r, self.referer) and len(self.imageList) > 0:
            return True
        return False

    def download(self, targetFolder='temp\\pixiv'):
        dt = timeit.default_timer()

        destinationFolder = os.path.join(
            targetFolder, f'[{self.artistID}] - {self.artist}\\[{self.id}] - {self.title.translate(str.maketrans("", "", string.punctuation))}')
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
        try:
            with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
                metadata.write(f'''
                Album URL: {self.referer}
                Title: {self.title}
                Number of images: {len(self.imageList)}
                Total Size: {size:,} bytes
                Tags: {self.tags}
                ''')
        except UnicodeEncodeError:
            pass

        time = timeit.default_timer()-dt

        print(
            f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, url, referer):
        self.url = url
        self.referer = referer
        self.image = sess.get(self.url, headers={'referer': url})
        self.size = int(self.image.headers["Content-Length"])
        self.name = os.path.basename(self.url)
        self.time = self.image.elapsed.total_seconds()

    def download(self, destinationFolder='temp\\pixiv'):
        with open(os.path.join(destinationFolder, self.name), 'wb') as img:
            img.write(self.image.content)


class Artist:
    def __init__(self, url):
        self.url = url
        self.id = self.regex_id()
        self.all = sess.get(
            f'https://www.pixiv.net/ajax/user/{self.id}/profile/all', headers={'referer': self.url})
        self.illusts = list(self.all.json()["body"]["illusts"].keys())
        randomIllust = random.choice(self.illusts)
        self.name = sess.get(
            f'https://www.pixiv.net/ajax/user/{random.randint(1000000, 9999999)}/illusts?ids[]={randomIllust}').json()["body"][f"{randomIllust}"]["userName"]
        self.targetFolder = os.path.join(
            'temp\\pixiv', f'[{self.id}] - {self.name}')

    def regex_id(self):
        q = re.search(r'(?<=id=)[0-9]+', self.url)
        if q:
            return q.group(0)

    def download(self, numStart=0):
        numEnd = len(self.illusts)
        for illust in self.illusts[numStart:numEnd]:
            Album(
                f'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust}').download()
        compile_artist(self.targetFolder)
