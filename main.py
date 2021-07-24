import Youtube
import Spotify
import pause
from datetime import datetime, timedelta

def main():
    prevListCount = 0
    while(True):
        tomorrow = datetime.now() + timedelta(days = 1)
        yt = Youtube.getToken("mcballer815")
        sp = Spotify.getToken("monkeyballer98")
        print("Tokens Updated")

        listId, listCount = Youtube.getPlaylistInfo(yt, "Spotify Transfer")
        ytSongs = Youtube.getSongs(yt, listId, listCount)
        print("Youtbe Songs Retrieved")
        if listCount < prevListCount:
            Spotify.addSongs(sp, ytSongs, 0)
            print("Songs Added to Spotify")
        elif listCount > prevListCount:
            start = listCount - (listCount-prevListCount)
            Spotify.addSongs(sp, ytSongs, start)
            print("Songs Added to Spotify")
        else:
            print("Already Updated")
        prevListCount = listCount
        pause.until(tomorrow)

if __name__ == "__main__":
    main()
