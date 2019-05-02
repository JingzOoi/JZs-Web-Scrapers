from requests_html import HTMLSession

sess = HTMLSession()

page = sess.get('https://jaiminisbox.com/reader/read/kaguya-wants-to-be-confessed-to/en/0/144/page/1')
page.html.render()

img = page.html.find('img.open', first=True)
imgLink = img.attrs["src"]

image = sess.get(imgLink)
with open('1.png', 'wb') as f:
    f.write(image.content) 
