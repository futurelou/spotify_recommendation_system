import pandas as pd
from pandas import DataFrame, read_json, json_normalize
from pathlib import Path
import os, json
import numpy as np
import glob
import sqlalchemy

#############################################################################################################3
# do not run this

#json_files = (r"C:\Users\louie\OneDrive\Documents\Sound Recordings\spotify_million_playlist_dataset\data")
engine = sqlalchemy.create_engine(
    'mssql+pyodbc://@' + 'LOUIS-PC' + '/' + 'songs' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')

# putting all of the music files into a list makes accessing them easier
def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    return all_files


songs = get_files(json_files)

#opening all of the jsons
for i in songs:
        f = open(i)
        data = json.load(f)

        playlists = data['playlists']

        df = []
        songnames = {}
        for i in range(len(playlists)):

            tracks = playlists[i]['tracks']
# filtering the tracks for duplicates by checking in the dictionary for similar track names
            df1 = pd.DataFrame(tracks)
            if len(songnames) == 0:
                songdict = df1['track_name'].to_dict()
                songnames.update(songdict)
                continue
            for i in df1['track_name']:
                key = len(songnames)+1
                if i not in songnames.values():
                    songnames.update({key: i})
                elif i in songnames.values():
                    df1 = df1[df1['track_name'] != i]

            df.append(df1)


            merged = pd.concat(df)

            merged.to_sql('songs_db', engine,if_exists='append')
