from requests_html import HTMLSession

sess = HTMLSession()

class Series:
    def __init__(self, url):
        self.url = url
        self.page = sess.get(self.url)
        self.chapters = [link.attrs["href"] for link in self.page.html.find('.group', first=True).find('.title a')]
        self.chapterCount = len(self.chapters)

class Chapter:
    def __init__(self, firstPageURL):
        self.firstPage = sess.get(firstPageURL)
        self.firstPage.html.render()
        pageNav = self.firstPage.html.find('.topbar_right.tbtitle', first=True)
        self.pages = [link.attrs["href"] for link in pageNav.find('li a')]
        self.pageCount = len(self.pages)

url = 'https://jaiminisbox.com/reader/series/kaguya-wants-to-be-confessed-to/'

print(Chapter('https://jaiminisbox.com/reader/read/kaguya-wants-to-be-confessed-to/en/0/144/page/1').pages)