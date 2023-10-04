import pyodbc
import pandas as pd
import sqlalchemy
import spotipy
from spotipy import util
import time

# api keys
cid= "key"
sid = "key"

# quering from the database
engine = sqlalchemy.create_engine('mssql+pyodbc://@' + 'LOUIS-PC' + '/' + 'songs' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')

query = 'select * from album'

# reading into a pandas df
table = pd.read_sql(query,engine)

track_uri = table['track_uri']

# authentication stuff
username = 'louie123hjjh'
token = util.prompt_for_user_token(
    username=username,
    scope="user-read-recently-played",
    client_id=cid,
    client_secret=sid,
    redirect_uri="http://localhost:8888/callback"
)
sp = spotipy.Spotify(auth=token)

df = track_uri

merged = pd.DataFrame()

# reading the df in chucks in order to not have huge requests
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

for i in chunker(df,100):
    #time.sleep(1)
#adding audiofeatures into each of the songs
    audiofeatures = sp.audio_features(i)
    dictionary = audiofeatures

    df1 = pd.DataFrame(dictionary)
    merged = pd.concat([merged,df1])

merged.to_csv('musicdata')








