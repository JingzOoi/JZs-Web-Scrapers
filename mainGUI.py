import PySimpleGUI as sg
import eduComic_scraper
import zeroChan_scraper
import eduCafe_scraper
import danbooru_scraper
import yandere_scraper

while True:

    url = sg.PopupGetText('URL here: ')

    if url is None:
        break

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
        sg.Popup('Site not supported.')
        break

    if album.valid == False:
        sg.PopupError('Invalid Tag')
        break

    if page_specific == True:

        layoutMenu = [
            [sg.Text(
                f'{album.tag} \nWhat do you want to do with it?')],
            [sg.Button('Download first 10 pages\' worth', key='__btn1__')],
            [sg.Button('Download specific pages\' worth', key='__btn2__')],
            [sg.Button('Cancel', key='__btn3__')]
        ]
    else:
        layoutMenu = [
            [sg.Text(
                f'{album.title} | \n{album.imageCount} images found.\nWhat do you want to do with it?')],
            [sg.Button('Download all', key='__btn1__')],
            [sg.Button('Cancel', key='__btn3__')]
        ]

    menu = sg.Window('Menu', layoutMenu)

    eventMenu, valuesMenu = menu.Read()

    menu.Close()

    if eventMenu == '__btn1__':
        album.download()
    elif eventMenu == '__btn2__' and page_specific == True:
        num = int(sg.PopupGetText('Pages: '))
        album.download(num)
    elif eventMenu == '__btn3__' or (eventMenu == '__btn2__' and page_specific == False):
        break
