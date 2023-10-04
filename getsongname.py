import pandas as pd
import sqlalchemy



# this talks to the database and finds the song we are looking for
def return_song(prediction):
    engine = sqlalchemy.create_engine('mssql+pyodbc://@' + 'LOUIS-PC' + '/' + 'songs' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')

    query = f"select * from album where track_uri = '{prediction}'"

    table = pd.read_sql(query,engine)

    return table[['artist_name', 'track_name', 'track_uri']]
