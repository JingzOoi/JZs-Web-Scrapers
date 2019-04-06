# JZs-Web-Scrapers
JZ's Web Scrapers. More like 'scrapers that are useful for my lazy ass'.
<ol>
    <li><a href='#loadingbarpy'>loadingBar.py</a></li>
    <li><a href='#zerochanpy'>zeroChan.py</a></li>
    <li><a href='#educomicpy'>eduComic.py</a></li>
</ol>


<hr>

<h2>loadingBar.py</h2>
<h3>Because some files might need this, and I'm not smart enough to use other ones.</h3>
Not a scraper, but other scrapers might use this as a separate module.
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

<h2>zeroChan.py</h2>
<h3>Download images from the image board <a href="https://www.zeroChan.net">ZeroChan</a>.</h3>

<h3>Additional modules:</h3>
<ul>
    <li><a href="https://html.python-requests.org/">requests-html</a></li>
    <li>loadingBar.py (this repo)</li>
</ul>
<h3>Usage:</h3>
<pre>
    import zeroChan, loadingBar
    url = f'https://www.zerochan.net/{tag}'
    collection = zeroChan.Collection(url)
    collection.download()
</pre>
Note: the .download() function can take in an integer to indicate the number of pages to loop through, but it's defaulted to 10. All images will be downloaded to '\temp\zeroChan\{tag}' by default.

Also can be done:

<pre>
    import zeroChan
    url = f'https://www.zerochan.net/{tag}'
    collection = zeroChan.Collection(url)
    print(collection.imageCount)
</pre>

Attributes of class Collection:
<ul>
    <li>.url (str)</li>
    <li>.imageList (list)</li>
    <li>.imageCount (int)</li>
    <li>.tag (str)</li>

</ul>

To do: add validation

<hr>

<h2>eduComic.py</h2>
<h3>Downloads albums off the NSFW website nhentai.net.</h3>
<h3>Additional modules:</h3>
<ul>
    <li><a href="https://html.python-requests.org/">requests-html</a></li>
    <li>loadingBar.py (this repo)</li>
</ul>
<h3>Usage:</h3>
<pre>
    import eduComic, loadingBar
    url = 'https://nhentai.net/g/{6-digit-number}/'
    album = eduComic.Album(url)
    album.download()
</pre>
or:
<br>
<pre>
    import eduComic, loadingBar
    url = '{6-digit-number}'
    album = eduComic.Album(url)
    album.download()
</pre>
Note: Will be saved to \temp\eduComic\{6-digit-number} on default.

Also can be done:
<pre>
    import eduComic
    url = '{6-digit-number}'
    album = eduComic.Album(url)
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
    <li>.favourites (int)</li>
</ul>

<hr>
