from bs4 import BeautifulSoup                               # HTML scraper and parser
import requests                                             # Fetching HTML data from websites


# Getting the website HTML
def get_HTML_content(website:str) -> BeautifulSoup:
    '''
    Fetches the HTML content of the webpage. Returns a BeautifulSoup object.
    website: webpage's URL
    '''
    source = requests.get(website).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

def get_avatar_frame(HTML:BeautifulSoup):
    try:
        avatar_frame_div = HTML.find('div', class_='profile_avatar_frame')
        frame = avatar_frame_div.img['src']
    except:
        frame = None

    return frame


html = get_HTML_content('https://steamcommunity.com/id/customurlalreadyused/')
frame = get_avatar_frame(html)
print(frame)