import eduComic_scraper
import zeroChan_scraper
import eduCafe_scraper
import danbooru_scraper

url = input("URL here: ")
print('Looking for images...')

if 'zerochan' in url:
    album = zeroChan_scraper.Collection(url)
elif 'danbooru' in url:
    album = danbooru_scraper.Collection(url)
elif 'nhentai' in url or len(url) == 6:
    album = eduComic_scraper.Album(url)
elif 'hentai.cafe' in url:
    album = eduCafe_scraper.Album(url)

ans = input(f'{album.imageCount} images found within the first 10 pages. Download? Y/N ').lower()
if ans == 'y':
    album.download()
elif ans == 'n':
    print("\nExit.\n")
    exit()
else:
    try:
        a = int(ans)
        album.download(a)
    except:
        print("An error has occured.")
        exit()