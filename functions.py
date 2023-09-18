import requests, creds
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError

uri = creds.mongo_uri
client_id = creds.client_id
client_secret = creds.client_secret

def test_print(name):
    print("We in")
    print(name)
    return

def init_db():
    global client
    global mydb
    global mycol
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    mydb = client["TicketFinder"]
    mycol = mydb["users"]

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def login(widget):
    global username
    username = widget.login_page.username_line.text()

    try:
        response = mycol.find_one({ "username" : username })
        if response == None:
            widget.login_page.error_label.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#de0000;\">User {} was not found. Create a new account.</span></p></body></html>".format(username))
            widget.login_page.error_label.setVisible(True)
            return None
        else:
            print("Logging {} in.".format(username))
            return response
    except Exception as e:
        print(e)

def create_account(widget):
    global username
    username = widget.login_page.username_line.text()

    try:
        response = mycol.insert_one({ "username" : username })
        print("User {} was created successfully.".format(username))
        return response
    except DuplicateKeyError:
        widget.login_page.error_label.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#de0000;\">User {} already exists.</span></p></body></html>".format(username))
        widget.login_page.error_label.setVisible(True)
        return None
    except Exception as e:
        print(e)

def get_user_pref(username):
    response = mycol.find_one({ "username" : username },{ "_id": 0, "pref": 1 })
    return response

def update_user_settings():
    u_state = input("Which state would you prefer to attend shows in?\nState: ")

    try:
        mycol.update_one({ "username" : username }, { "$set" : { "pref.state" : u_state } })
        print("Settings updated.")
    except Exception as e:
        print("Something went wrong while deleting from favorites.")
        print(e)

def get_favorites():
    response = mycol.find({ "username" : username },{ "_id": 0, "favorites.artist": 1 })

    artistList = []
    for x in response:
        try:
            for y in x["favorites"]:
                name = y["artist"]
                artistList.append(name)
            return artistList
        except KeyError:
            print("There are no artists in your favorites yet.")
            return []
        
def get_favorites_ids(username):
    response = mycol.find({ "username" : username },{ "_id": 0, "favorites.id_num": 1 })

    artistList = []
    for x in response:
        try:
            for y in x["favorites"]:
                name = y["id_num"]
                artistList.append(name)
            return artistList
        except KeyError:
            print("There are no artists in your favorites yet.")
            return []

def get_artists(artist): 
    artist_request = requests.get("https://api.seatgeek.com/2/performers?q={}&client_id={}".format(artist, client_id)).json().get("performers")
    artist_list = []
    for x in artist_request:
        item = {
            "id_num": x["id"],
            "artist": x["name"],
            "image": x["image"]
        }
        artist_list.append(item)
    return artist_list

def set_favorite_artist(username, artistInfo):

    response = mycol.find({ "username" : username, "favorites.artist": artistInfo["artist"] })
    responseLen = len(list(response))
    
    if responseLen == 0:
        try:
            mycol.update_one({ "username" : username }, { "$push" : {"favorites": artistInfo}}, upsert = True)
            print("{} was added to your favorites list.".format(artistInfo["artist"]))
        except Exception as e:
            print(e)
    else:
        print("Artist already in favorites.")

def remove_favorite_artist():
    artistList = get_favorites()

    if len(artistList) == 0 :
        print("There are no artists in your favorites yet.")
        return
    
    print(artistList)
    
    artistToDelete = input("Which artist (must match case) do you want to remove? Hit enter to cancel.\n")

    if artistToDelete in artistList:
        try:
            mycol.update_one({ "username" : username }, { "$pull" : { "favorites" : { "artist" : artistToDelete } } })
            print("{} was removed from your favorites list.".format(artistToDelete))
        except Exception as e:
            print("Something went wrong while deleting from favorites.")
            print(e)
    else:
        print("No artist deleted. No artist selected or name was misspelled.")

def get_events(username):
    artist_ids_list = get_favorites_ids(username)
    artist_ids = ",".join(str(x) for x in artist_ids_list)
    state = get_user_pref(username)["pref"]["state"]
    
    if len(artist_ids_list) > 0:
        events = requests.get("https://api.seatgeek.com/2/events?performers.id={}&venue.state={}&client_id={}".format(artist_ids, state, client_id)).json()

        counter = 0
        for x in events["events"]:
            for y in x["performers"]:
                if y["id"] in artist_ids_list:
                    events["events"][counter]["artist_name"] = y["name"]
                    events["events"][counter]["image_url"] = y["image"]
                    break
            counter = counter + 1

        return events
    else:
        return { "events": []}
        