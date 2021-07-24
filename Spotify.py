import spotipy

def getToken(username):
    try:
        # client_id and client_secret come from app created in Spotify developer account
        token = spotipy.util.prompt_for_user_token(username, "user-library-modify user-read-private",
        client_id='be3ff50517384a24907a8eed8c80bca1', 
        client_secret='7e38a4328695403b902462610db339c6',
        redirect_uri='http://google.com/')
    except:
        remove(f".cache-{username}")
        
    #Create spotify object
    return spotipy.Spotify(auth=token)

def addSongs(sp, songs, start):
    # Search for each Youtube Music song in Spotify and add it to "Liked Songs" playlist in Spotify"
    i = start
    while i < len(songs):
        result = sp.search(q=songs[i], limit=1, type='track', market="from_token") # Spotipy search function to get song ID needed to add song
        try: # try to add song to Spotify. If unable, make note in logs
            sp.current_user_saved_tracks_add(tracks=[result['tracks']['items'][0]["id"]])
            print(songs[i])
        except:
            print("Unable to add: " + songs[i])
        i+=1