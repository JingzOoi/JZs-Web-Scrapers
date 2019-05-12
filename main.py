import eduComic_scraper
import zeroChan_scraper
import eduCafe_scraper
import danbooru_scraper
import yandere_scraper

url = input("URL here: ")
print('Looking for images...')

if 'zerochan.net' in url:
    album = zeroChan_scraper.Collection(url)
    page_specific = True
elif 'danbooru.donmai.us' in url:
    album = danbooru_scraper.Collection(url)
    page_specific = True
elif 'yande.re' in url:
    album = yandere_scraper.Collection(url)
    page_specific = True
elif 'nhentai.net' in url:
    album = eduComic_scraper.Album(url)
    page_specific = False
elif 'hentai.cafe' in url:
    album = eduCafe_scraper.Album(url)
    page_specific = False
else:
    print('Link Error. Site might not be supported.')
    exit()

if page_specific == True:
    cli_page_specific = f'''
{album.name} | {album.imageCount} images found.
What do you want to do with it?
[1] Download first 10 pages' worth of content
[2] Download specific pages' worth of content
[3] Exit

> '''
else:
    cli_page_specific = f'''
{album.name} | {album.imageCount} images found.
What do you want to do with it?
[1] Download all
[2] Exit

> '''
print(cli_page_specific, end='')
ans = int(input())
try:
    if ans == 1:
        album.download()
    elif ans == 2 and page_specific == True:
        album.download(int(input('Page count: ')))
    else:
        print('Exit.')
        exit()
except Exception as e:
    exit(f'Script exit with message: {e}')
