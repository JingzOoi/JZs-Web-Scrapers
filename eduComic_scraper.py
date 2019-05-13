from requests_html import HTMLSession
import os
import loadingBar
import timeit
from time import sleep

sess = HTMLSession()


class Album:
    def __init__(self, url: str):

        if len(url) <= 6:
            self.url = f'https://nhentai.net/g/{url}/'
        elif 'nhentai' in url:
            self.url = url
        else:
            print("Invalid link.")
            exit()

        self.magicNumber = self.url.split('/')[-2]
        self.page = sess.get(self.url)
        self.valid = self.verifyTag()
        if self.valid == True:
            self.title = self.searchMeta(self.page)["title"]
            self.tags = self.searchMeta(self.page)["tags"]
            self.album = [
                f'https://nhentai.net{thumb.attrs["href"]}' for thumb in self.page.html.find('.gallerythumb')]
            self.imageCount = len(self.album)
            self.favourites = int(self.page.html.find(
                '.nobold', first=True).text.strip('()'))
            self.name = self.title

    def verifyTag(self):
        if 'error' in self.page.html.find('.container', first=True).attrs['class']:
            return False
        return True

    def searchMeta(self, page):

        metaDict = {}

        for meta in page.html.find('meta'):
            try:
                if meta.attrs["name"] == "twitter:title":
                    metaDict["title"] = meta.attrs["content"]

                if meta.attrs["name"] == "twitter:description":
                    metaDict["tags"] = meta.attrs["content"]

            except KeyError:
                continue

        return metaDict

    def download(self):
        dt = timeit.default_timer()
        destinationFolder = f'temp\\eduComic\\{self.magicNumber}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0

        for pageNum, image in enumerate(self.album, start=1):

            img = Image(image)

            with open(os.path.join(destinationFolder, img.name), 'wb') as file:
                file.write(img.image.content)
            size += img.size
            loadingBar.loadingBar(
                self.imageCount, pageNum, message=f'{pageNum}/{self.imageCount} {img.name}')

            sleep(img.time)

        print('\nDownloading operations complete.\nCreating metadata file.')

        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(
                f'Album URL: {self.url}\nTitle: {self.title}\nNumber of pages: {self.imageCount}\nTags: {self.tags}\nTotal Size: {size:,} bytes')

        time = timeit.default_timer()-dt

        print(
            f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, pageURL):
        self.srcPage = sess.get(pageURL)
        self.link = self.srcPage.html.find(
            '#image-container', first=True).find('img', first=True).attrs["src"]
        self.image = sess.get(self.link)
        self.size = int(self.image.headers["Content-Length"])
        self.name = os.path.basename(self.link)
        self.time = self.image.elapsed.total_seconds()
