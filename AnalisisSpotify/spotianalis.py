import functions as fn
import pandas as pd
import numpy as np


client_id = "c0106e614a6e4d2ebca46fd5401e7be4"
client_secret = "dfb41a1a744f416db305ca6185074c2d"

sp = fn.authManager(client_id, client_secret)
playList = fn.serchPlaylistByName(sp, "Balada romantica 60's 70's & 80's Vol. 1")
playlist_tracks = fn.getAllItems(sp, playList)
tracks = fn.getTracksData(playlist_tracks)

tracksData = pd.DataFrame(tracks)
print(tracksData)

features = fn.getAudioFeatures(sp, tracksData["Id Track"].tolist())
featuresData = pd.DataFrame(features)
featuresData = featuresData.drop(['type','id','uri','track_href','analysis_url','duration_ms'],axis=1)

playListData = pd.concat([tracksData,featuresData],axis=1)
stadisticData = playListData.describe()

playListData.to_excel("playlistdata.xlsx", index=False)
print(playListData)
print(stadisticData)

with open('canciones.txt', 'w',encoding="utf-8") as f:
    # Iterar sobre cada fila del dataframe
    for index, row in playListData.iterrows():
        # Obtener el nombre de la canción y el nombre del artista
        song_name = row['Track Name']
        artist_name = row['Artist Name']
        
        # Escribir el nombre de la canción y el nombre del artista en el archivo de texto plano
        f.write(f'{song_name} - {artist_name}\n')