# JZs-Web-Scrapers
JZ's Web Scrapers. More like 'scrapers that are useful for my lazy ass'.

<li>eduComic.py</li>

<h2>eduComic.py</h2>
<h3>Downloads albums off the NSFW website nhentai.net.<h3>
<p>
Usage:
<br>
<pre>
import eduComic
url = 'https://nhentai.net/g/{6-digit-number}/'
album = educomic.Album(url)
album.download()
</pre>
<br>
or:
<br>
<pre>
import eduComic
url = '{6-digit-number}'
album = educomic.Album(url)
album.download()
</pre>
Will be saved to \temp\eduComic\{6-digit-number} on default.
</p>