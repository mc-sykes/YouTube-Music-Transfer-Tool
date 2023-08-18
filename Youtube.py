import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pickle
import os
import math

def getToken(username):
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = ""

    # Look for stored API client for user. If not found create one
    try:
        # Grab previous credentials
        with open('yt-'+username, 'rb') as creds_file:
            yt = pickle.load(creds_file)
    except:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        yt = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        # Save client credentials
        with open('yt-'+username, 'ab') as creds_file:
            pickle.dump(yt, creds_file)

    return yt

def getPlaylistInfo(yt, playlistName):
    # Request to gather playlist info
    response = yt.playlists().list(
        part="snippet,contentDetails",
        maxResults=50,
        mine=True
    ).execute()

    # pInfo contains all playlist objects
    playlists = response["items"]

    i = 0
    playlistId = ""
    playlistCount = 0

    # Search for playlist named Spotify Transfers. Grab it's youtube ID and store in playlistId. Grab number of songs in it and store in playlistCount
    found = False
    while i < len(playlists) and not found:
        if playlists[i]["snippet"]['title'] == playlistName:
            playlistId = playlists[i]["id"]
            playlistCount = playlists[i]["contentDetails"]["itemCount"]
            found = True
        i+=1
    return playlistId, playlistCount

def getSongs(yt, playlistId, playlistCount):

    # Request to gather the songs in selected playlist 
    response = yt.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlistId
    ).execute()

    # sInfo contains all song objects
    songInfo = response["items"]

    songs = []

    # Grab each song name and artist name (Youtube music format "Artist - Topic")
    for sItem in songInfo:
        songName = sItem["snippet"]["title"]
        artist = sItem["snippet"]["videoOwnerChannelTitle"]
        artist = artist.split(" - Topic")[0]
        songs.append(songName + " " + artist)
        #print(songs)
    
    # loopNum calculates how many more calls are needed to get full playlist
    loopNum = math.floor(playlistCount/50)
    #Grab next set of results
    for loop in range(loopNum):
        response = yt.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlistId,
            pageToken=response["nextPageToken"]
        ).execute()

        songInfo = response["items"]

        # Grab each song name and artist name (Youtube music format "Artist - Topic")
        for sItem in songInfo:
            songName = sItem["snippet"]["title"]
            artist = sItem["snippet"]["videoOwnerChannelTitle"]
            artist = artist.split(" - Topic")[0]
            songs.append(songName + " " + artist)
    return songs
