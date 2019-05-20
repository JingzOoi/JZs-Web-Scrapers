import eduComic_scraper
import zeroChan_scraper
import eduCafe_scraper
import danbooru_scraper
import yandere_scraper
import pixiv_scraper
import PySimpleGUI as sg


def create_album(url):
    if url is None:
        exit('Invalid Link')
    elif 'pixiv.net' in url:
        album = pixiv_scraper.Album(url)
        page_specific = False
    elif 'zerochan.net' in url:
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
        raise Exception('Link Error. Site might not be supported.')

    if album.valid == False:
        raise Exception('Invalid Tag.')

    return album, page_specific


layout = [
    [sg.Text('Enter URL here: ', key='_url_')],
    [sg.InputText(key='_url_')],
    [sg.OK(), sg.Cancel()]
]

window = sg.Window('JZ\'s Web Scrapers', layout)


while True:
    event, values = window.Read()

    if event == 'Cancel' or event is None:
        break
    else:
        try:
            album, page_specific = create_album(values['_url_'])
        except Exception as e:
            sg.PopupError(e)
            break

        if page_specific == True:
            layout2 = [
                [sg.Text(f'{album.name}')],
                [sg.Button('Download first 10 pages', key='_btn1_')],
                [sg.Button('Download specific pages', key='_btn2_')],
                [sg.Cancel()]
            ]
        else:
            layout2 = [
                [sg.Text(f'{album.name} | {album.imageCount} images found.')],
                [sg.Button('Download album', key='_btn1_')],
                [sg.Cancel()]
            ]

        window2 = sg.Window('Options', layout2)
        window.Close()
        event2, values2 = window2.Read()
        window2.Close()
        if event2 == '_btn1_':
            time, size = album.download()
            sg.Popup(
                f'{album.imageCount} images downloaded.\n{round(time, 2)} seconds used.')
        elif event2 == '_btn2_':
            pageCount = int(sg.PopupGetText('Page count: '))
            time, size = album.download(pageCount)
            sg.Popup(
                f'{album.imageCount} images downloaded.\n{round(time, 2)} seconds used.')
        else:
            break

    break
