# JZs-Web-Scrapers
JZ's Web Scrapers. More like 'scrapers that are useful for my lazy ass'.
<ol>
    <li>loadingBar.py</li>
    <li>eduComic.py</li>
</ol>


<hr>

<h2>loadingBar.py</h2>
<h3>Because some files might need this, and I'm not smart enough to use other ones.</h3>
Not a scraper, but other scrapers might use this.
<br>
<h3>Usage:</h3>

<pre>
from loadingBar import loadingBar
for i in range(500):
    loadingBar(500, i)
</pre>

Parameters:
<ul>
    <li>maximumNumber: the maximum number</li>
    <li>currentNumber: the current number</li>
    <li>(optional) message: message to be displayed. Formatted strings recommended.</li>
    <li>(optional) startingNumber: the starting number. For when the loop does not start from 1.</li>
</ul>

<hr>

<h2>eduComic.py</h2>
<h3>Downloads albums off the NSFW website nhentai.net.</h3>
<h3>Additional modules:</h3>
<ul>
    <li><a href="https://html.python-requests.org/">requests-html</a></li>
</ul>
<h3>Usage:</h3>
<pre>
import eduComic
url = 'https://nhentai.net/g/{6-digit-number}/'
album = educomic.Album(url)
album.download()
</pre>
or:
<br>
<pre>
import eduComic
url = '{6-digit-number}'
album = educomic.Album(url)
album.download()
</pre>
Note: Will be saved to \temp\eduComic\{6-digit-number} on default.

Also can be done:
<pre>
import eduComic
url = '{6-digit-number}'
album = educomic.Album(url)
print(album.title)
</pre>

Attributes of class Album:
<ul>
    <li>.url (str)</li>
    <li>.magicNumber (str)</li>
    <li>.page (Response)</li>
    <li>.title (str)</li>
    <li>.tags (str)</li>
    <li>.album (list)</li>
    <li>.pageCount (int)</li>
</ul>

<hr>
