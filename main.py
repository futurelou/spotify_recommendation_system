import pandas as pd
from userdata import getuserdata
from sklearn.neighbors import KNeighborsClassifier
from getsongname import return_song
import spotipy
from spotipy import util

cid= 'Place Holder'
secret = 'Place Holder'

userdata = getuserdata(cid,secret)
musicdata = pd.read_csv('musicdata')

#saving labels
musicdatalabs = musicdata['uri']
userdatalabs = userdata['uri']

##dropping columns
musicdata_clean = musicdata.drop(['Unnamed: 0', 'type', 'id', 'track_href', 'analysis_url', 'uri'   ], axis=1)
userdata_clean = userdata.drop(['uri','type', 'id' ,'track_href', 'analysis_url' ,'track.id' , 'track.name' , 'track.popularity', 'track.duration_ms'], axis=1)

#getting the mean of all of the recntly played columns
onesongmean = userdata_clean.mean()

# putting into a data frame
onesongmeandf = pd.DataFrame(onesongmean)

# transposing the dataframe
onesongdf = onesongmeandf.T.reset_index()
onesongdf = onesongdf.drop('index', axis=1)

#using knn to find the nearest neightbor this will be the reccommended song
neigh = KNeighborsClassifier(n_neighbors=5)
neigh.fit(musicdata_clean, musicdatalabs)

# getting the prediction
prediction = neigh.predict(onesongdf)

# reading into a data frame
predf = pd.DataFrame(prediction)


# pulling the prediction out of the data frame
songpredistion = predf[0][0]

# gradding the song
songrec = return_song(songpredistion)

#pulling it out of the array
songrecuri = songrec['track_uri'][0]

# authentication of spotify user
username = 'louie123hjjh'
token = util.prompt_for_user_token(
    username=username,
    scope="user-modify-playback-state",
    client_id=cid,
    client_secret=secret,
    redirect_uri="http://localhost:8888/callback"
)
sp = spotipy.Spotify(auth=token)

# queing the song on my spotify
sp.add_to_queue(songrecuri)
