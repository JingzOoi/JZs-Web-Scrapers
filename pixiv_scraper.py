from requests_html import HTMLSession
import os, loadingBar, timeit

sess = HTMLSession()

url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=74251632'

page = sess.get(url)

print(page.html.find('a'))