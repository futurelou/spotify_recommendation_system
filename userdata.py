import spotipy
from spotipy import util
import pandas as pd


# this function returns the user of interest recently 50 played songs
def getuserdata(cid, secret):

    username = 'louie123hjjh'
    token = util.prompt_for_user_token(
        username=username,
        scope="user-read-recently-played",
        client_id=cid,
        client_secret=secret,
        redirect_uri="http://localhost:8888/callback"
    )
    sp = spotipy.Spotify(auth=token)

    data = sp.current_user_recently_played(limit=10, after=None, before=None) #returns 50 songs
# getting the json all normalized
    tracks = data['items']

    df = pd.json_normalize(tracks)
# pylling the columns I want to look at
    recent_songs = df[['track.name', 'track.popularity', 'track.duration_ms', 'track.id' ]]

# getting audio features from the songs song characteristics
    dictionary = sp.audio_features(recent_songs['track.id'])

# putting data into a dictionary
    df1 = pd.DataFrame(dictionary)

# merging the characteristics with the main df
    df_merged = recent_songs.join(df1, lsuffix='track.id', rsuffix='id')


    return df_merged





