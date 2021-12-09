### IMPORTS #########
from flask import Flask, send_from_directory    # The Main Flask App thing, and send_from_directory to serve static files from local directory
import requests                                 # for API requests
import json                                     # To parse and send JSON objects to and from the svelte front-end
import hashlib                                  # For getting the Hash256 of an inventory to detect changes
from datetime import datetime                   # Logging the time at which data was fetched
import os                                       # Checking if file exists on local path
from typing import Dict, Tuple, List, Union     # Type hinting


### CONSTANTS #########
URL = 'https://steamcommunity.com/id/{}/inventory/json/440/2'
URL_STEAM_PROFILE   = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}"
URL_STEAM_ID        = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}"
URL_ITEMS           = "https://steamcommunity.com/inventory/{}/440/2"
URL_TIME_PLAYED     = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={}&steamid={}&include_played_free_games=1&appids_filter[0]=440"
KEY_FILE            = "steam_api.key"
KEY                 = "XXXXXXXXXXXXX"
CACHE               = "cache"   # directory where the cached data is stored locally
UPDATE_PERIOD       = 86400     # 24h in seconds



### FUNCTIONS #########
def get_api_key() -> str:
    # Getting the Steam API key
    with open(KEY_FILE, 'r') as f:
        key = f.read().rstrip() # have to remove newlines on here but not on my PC? weird...
        print(key)
        return key

def f(item: dict) -> dict:
    '''
    Takes a TF2 Item Object and extracts only the relevant info. Returns a dict.
    '''
    return {
        'id'        : item['app_data']['def_index'],                                                # The item's in-game ID - only available on the vanityurl API for some reason...
        'name'      : item['name'],                                                                 # full name of the item
        'colour'    : item['name_color'] if item['tags'][0]['name'] != 'Unique' else 'f6d627',      # Rarity colour for name and border. Gotta hard-code the Unique Quality colour because the value on the API is piss.
        'quality'   : item['tags'][0]['name'],                                                      # Quality of this item: unique, genuine, strange, haunted, etc...
        'type'      : item['type'],                                                                 # Level X [weapon/item type]
        'image'     : f"https://community.akamai.steamstatic.com/economy/image/{item['icon_url']}", # item's inventory image
        'category'  : item['tags'][1]['name'],                                                      # (primary/secondary/melee) weapon, or crafting item, or cosmetic
        'desc'      : item['descriptions'],                                                         # the in-game description of the item, colour-coded
        'classes'   : [c['name'] for c in item['tags'][2:]] if len(item['tags']) > 2 else ""        # getting the classes that this item belongs to only if it's a weapon (weapon = > 2 tags)
    }

def f64(item: dict) -> dict:
    '''
    STEAMID64 API VERSION!! Takes a TF2 Item Object and extracts only the relevant info. Returns a dict.
    def_index not available, must use unique id instead
    tags.name is renamed to tags.internal_name
    '''
    return {
        'id'        : item['classid'],
        'name'      : item['name'],
        'colour'    : item['name_color'] if item['tags'][0]['internal_name'] != 'Unique' else 'f6d627',
        'quality'   : item['tags'][0]['internal_name'],
        'type'      : item['type'],
        'image'     : f"https://community.akamai.steamstatic.com/economy/image/{item['icon_url']}",
        'category'  : item['tags'][1]['internal_name'],
        'desc'      : item['descriptions'] if 'descriptions' in item else [],   # some items don't have the description property so we must check if it exists and give it an empty list if it doesn't
        'classes'   : [c['internal_name'] for c in item['tags'][2:]] if len(item['tags']) > 2 else ""
    }


def get_hash(data:dict) -> str:
    '''
    Takes the JSON data, converts it to a string, then calculates it SHA256 Hash.
    '''
    key = json.dumps(data).encode()
    hash256 = hashlib.sha256(key).hexdigest()

    return hash256


def fetch_items(user_url:str = 'customurlalreadyused'):
    '''
    Fetching JSON inventory data from a steam user's TF2 inventory using their Steam Profile URL. Returns their TF2 items, formatted.
    '''
    response = requests.get(URL.format(user_url))
    data = response.json()
    print(data)
    item_data = data['rgDescriptions']
    items = [f(item) for key, item in item_data.items()]

    return items

def fetch_items_by_id(steamid) -> Tuple[List[dict], int]:
    '''
    Fetching JSON inventory data from a steam user's TF2 inventory using their SteamID64. Returns their TF2 items, formatted.
    '''
    response = requests.get(URL_ITEMS.format(steamid))
    data = response.json()
    item_data = data['descriptions']
    items = [f64(item) for item in item_data]
    item_count = data['total_inventory_count']

    return items, item_count



def fetch_steamid64(vanityurl: str):
    '''
    Fetches a user's unique STEAMID64 using their profile URL. This ID is required to use the API.
    vanityurl: Their steam community /URL
    '''
    response    = requests.get(URL_STEAM_ID.format(KEY, vanityurl))
    data        = response.json()
    
    if data['response']['success'] == 1:
        steamid64   = data['response']['steamid']
        return steamid64
    
    else:
        print(f"No Steam user found with URL: {vanityurl}")
        return False


def fetch_steam_profile(steamid64: int):
    '''
    Fetches a user's Steam Profile info, such as avatar and username, using their STEAMID64.
    STEAMID64: A long string of numbers.
    '''
    valid, msg = validate_steamid(steamid64)
    if not valid:
        raise ValueError(msg)

    response    = requests.get(URL_STEAM_PROFILE.format(KEY, steamid64))
    data        = response.json()
    profile     = data['response']['players'][0]

    return profile


def validate_steamid(steamid64) -> Union[bool, str]:
    '''
    Checks if a steamid input is valid: 17 digit long number.
    '''
    try:
        int(steamid64)
    except:
        return False, "STEAMID64 must be a string only containing numbers"
    
    if len(steamid64) != 17:
        return False, "STEAMID64 must be exactly 17 digits"
    
    return True, "ID is valid"


def fetch_playtime(steamid: int) -> int:
    '''
    Looks up how much time a user has played in TF2
    '''
    response        = requests.get(URL_TIME_PLAYED.format(KEY, steamid))
    data            = response.json()

    # In case we can't find TF2 in the Steam User's game stats
    if 'games' not in data['response']:
        print(f'User {steamid} has never played TF2 or profile is private.')
        return False

    minutes_played  = data['response']['games'][0]['playtime_forever']
    hours_played    = round(minutes_played / 60)

    return hours_played


def load_local_data(steamid) -> dict:
    '''
    Checks if a user's backpack data is stored locally. If it is and it has been updated recently, return it.
    Otherwise, throw an error.
    '''
    user_file = f'{CACHE}/{steamid}.json'

    # If we don't have the file saved locally
    if not os.path.isfile(user_file):
        print(f'File {steamid}.json not found on local cache')
        return False

    # If the file hasn't been updated recently enough
    with open(user_file) as f:
        data = json.load(f)

        time_diff = datetime.now().timestamp() - data['last_updated']
        print(time_diff)

        if time_diff > UPDATE_PERIOD:
            print("File hasn't been updated in more than 24h hours. Must re-downloaded data.")
            return False
        
        # If it was found and data is fresh, return it
        return data





### INITIALISING APP #########
app = Flask(__name__)


### ROUTES #########
# SVELTE :: Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('svelte-frontend/public', 'index.html')
# SVELTE :: Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('svelte-frontend/public', path)

# API :: Fetching the user's TF2 backpack using their steam profile URL
@app.route("/backpack/<steam_URL>")
def get_backpack2(steam_URL: str):
    # 1. check if the URL provided is already in the STEAMID64 format. Otherwise it's a vanity url and use that to fetch the STEAMID
        # 1.1 fetch STEAMDID if specified with vanityurl
        # 1.2 display error if vanityurl does not exist
    # 2. check if the user's backpack is saved in the local cache
        # 2.1 if saved, check when it was last updated. If less than 24h ago, use cached version. Otherwise fetch data again.
        # 2.2 check inventory hash to see if there have been changes. if so, save the changes to the cache. Otherwise only change the last_updated property
    # 3. Fetch data (items, playtime, and profile info)
    # 4. Update cached data
    # 5. Return user data

    # STEP 1
    valid, msg = validate_steamid(steam_URL)
    steamid = steam_URL if valid else fetch_steamid64(steam_URL)
    if not steamid:
        return {'success': False, 'msg': 'No user found with that URL'}

    # STEP 2
    local_data = load_local_data(steamid)
    if local_data:
        return local_data
    
    # STEP 3
    profile = fetch_steam_profile(steamid)
    playtime = fetch_playtime(steamid)
    if not playtime:
        return {'success': False, 'msg': 'User has never played TF2, or profile is private'}

    items, item_count   = fetch_items_by_id(steamid)
    hash256             = get_hash(items)
    last_updated        = datetime.now().timestamp()

    backpack = {
        'steamid'       : steamid,
        'user_url'      : steam_URL,
        'username'      : profile['personaname'],
        'avatar'        : profile['avatarfull'],
        'playtime'      : playtime,
        'hash'          : hash256,
        'last_updated'  : last_updated,
        'item_count'    : item_count,
        'items'         : items,
        'success'       : True
    }

    # STEP 4
    with open(f'{CACHE}/{steamid}.json', 'w+') as f:
        json.dump(backpack, f)
    
    # STEP 5
    return backpack


### READING STEAM API KEY #########
KEY = get_api_key()


### RUNNING THE WEBSITE #########
if __name__ == '__main__':   
    app.run(debug=True)
