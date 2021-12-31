from bs4 import BeautifulSoup                               # HTML scraper and parser
import requests                                             # Fetching HTML data from websites
import re                                                   # REGEX to extract numbers from string


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
    '''
    Gets the link to a Steam user's profile frame, if they have one.
    '''
    try:
        avatar_frame_div = HTML.find('div', class_='profile_avatar_frame')
        frame = avatar_frame_div.img['src']
    except:
        frame = None

    return frame

def get_backpack_value(steamid:int):
    '''
    Gets the value of a user's backpack in [ref, keys, USD] from backpack.tf.
    steamid: SteamID64 of the user
    '''
    html = get_HTML_content(f'https://backpack.tf/u/{steamid}')                             # Getting the backpack.tf profile page of the user
    data = html.find('span', class_='refined-value')['title']                               # Getting the 'title' attribute of the 'refined-value' span
    print(data)

    values_str = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", data)    # Extracting all the number values from the string -> https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
    values_float = [float(x.replace(',', '')) for x in values_str]                          # Formating the strings of numbers into floats, while removing the thousands seperator
    
    # Formatting the data into a dictionary
    try:
        backpack_value = {
            'ref'   : int(values_float[0]),         # Convert to INT to remove decimals
            'keys'  : values_float[1],
            '$'     : round(values_float[2], 2)     # Convert to 2 decimal places 
        }
    # Failsafe in case there aren't enough values
    except:
        backpack_value = {
            'ref'   : 'N/A',
            'keys'  : 'N/A',
            '$'     : 'N/A'
        }

    return backpack_value


if __name__ == '__main__':
    html = get_HTML_content('https://steamcommunity.com/id/customurlalreadyused/')
    frame = get_avatar_frame(html)
    print(frame)

    get_backpack_value(76561198055543499)