# JZs-Web-Scrapers
JZ's Web Scrapers. More like 'scrapers that are useful for my lazy ass'.

1. <a href = '#webcomic_twitter.py'>webcomic_twitter.py</a>

# webcomic_twitter.py
Q: What does it do?  
A: it downloads image files from Twitter posts.

Q: Why <i>webcomic</i>_twitter?  
A: That's what I was intending to use it for.

Q: Why should I use this instead of clicking the images and saving them individually using "Save Image As..."?  
A: Because I'm a lazy bum and don't want to do that. You do you.

Q: Seems pretty overkill even for laziness.  
A: It's pretty useful for posts that have chapters and reply to each other, creating 20+ images in a chain. I don't want to download them one by one. Posts like this: https://twitter.com/sgin001/status/1079877836331134978 (Not paid to promote them btw)

<h2>Additional modules to install</h2>
<ul>
  <li><a href = 'https://www.crummy.com/software/BeautifulSoup'>bs4</a></li>
  <li><a href = 'http://docs.python-requests.org/en/master/'>requests</a></li>
</ul>

<h2>How to use</h2>
<ul>
  <li>Copy the Twitter post link into the clipboard.</li>
  <li>Run the script. [In powershell (Windows) / terminal (Mac): python webcomic_twitter.py <url>]</li>
</ul>

<h2>What you should expect will happen</h2>
<ul>
  <li>A path will be created along with the folders: .\temp\(twitter_handle)\(post_ID).</li>
  <li>The images will be saved in the (post_ID) folder.</li>
  <li>A metadata.txt file will be created, recording the source link, the Twitter handle, number of images downloaded, and the date and time the operation is performed.</li>
  <li>If the (twitter_handle) folder already exists, the new (post_ID) folder will be created under said folder.</li>
</ul>
