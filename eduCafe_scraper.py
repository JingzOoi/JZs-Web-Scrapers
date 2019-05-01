from requests_html import HTMLSession
import os, loadingBar, timeit

sess = HTMLSession()


class Album():
    def __init__(self, url):
        if len(url.split('/')) > 5 and '/manga/read' in url:
            self.url = '/'.join(url.replace('/manga/read', '').split('/')[:3])
        else:
            self.url = url
        self.page = sess.get(self.url)
        self.title = self.page.html.find('.x-column.last h3', first=True).text
        self.start = self.page.html.find('.x-btn.x-btn-flat', first=True).attrs["href"]
        self.album = [link.find('a', first=True).attrs["href"] for link in sess.get(self.start).html.find('ul.dropdown li')]
        self.imageCount = len(self.album)
        self.tags = [link.text for link in self.page.html.find('.x-column.last p', first=True).find('a')]

    def download(self):
        dt = timeit.default_timer()

        destinationFolder = f'temp\\eduCafe\\{self.title}'
        print(f'\nCreating folder {destinationFolder}.')

        os.makedirs(destinationFolder, exist_ok=True)
        print('Starting download operations.')

        size = 0

        for pageNum, image in enumerate(self.album, start=1):

            img = Image(image)

            with open(os.path.join(destinationFolder, img.name), 'wb') as file:
                file.write(img.image.content)

            size += img.size

            loadingBar.loadingBar(self.imageCount, pageNum, message=f'{pageNum}/{self.imageCount} {img.name}')

        print('\nDownloading operations complete.\nCreating metadata file.')
        
        with open(os.path.join(destinationFolder, 'metadata.txt'), 'w+') as metadata:
            metadata.write(f'Album URL: {self.url}\nTitle: {self.title}\nNumber of pages: {self.imageCount}\nTags: {self.tags}\nTotal Size: {size:,} bytes')

        time = timeit.default_timer()-dt
        
        print(f'\nAll operations complete. \nTotal time used: {round(time, 2):,} seconds\n')


class Image:
    def __init__(self, url):
        self.page = sess.get(url)
        self.link = self.page.html.find('.open', first=True).attrs['src']
        self.name = os.path.basename(self.link)
        self.image = sess.get(self.link)
        self.size = int(self.image.headers["Content-Length"])