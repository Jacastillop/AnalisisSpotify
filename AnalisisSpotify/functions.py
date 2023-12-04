import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def authManager(cliendId, secretId):
    auth_manager = SpotifyClientCredentials(client_id=cliendId, client_secret=secretId)
    return spotipy.Spotify(auth_manager=auth_manager)


def serchPlaylistByName(spotifyAuth, playlistName):
    playlists = spotifyAuth.search(q=playlistName, type="playlist")["playlists"][
        "items"
    ]
    playlist_id = playlists[0]["id"]
    return spotifyAuth.playlist_tracks(playlist_id, offset=0)


def getAllItems(spotifyAuth, playList):
    playlist_tracks = []
    cont = 0
    playlist_tracks += playList["items"]

    print("\n..Obteniendo Items..\n")
    while playList["next"]:
        cont += 1
        playList = spotifyAuth.next(playList)
        playlist_tracks += playList["items"]
        print(f"..Page {cont}..")
    print("Playlist completa\n")

    return playlist_tracks


def getTracksData(playlist_tracks):
    tracks = []

    for track in playlist_tracks:
        idTrack = track["track"]["id"]
        albumName = track["track"]["album"]["name"]
        trackName = track["track"]["name"]
        artistsName = track["track"]["artists"][0]["name"]
        durationMs = track["track"]["duration_ms"]
        popularity = track["track"]["popularity"]
        albumImage = track["track"]["album"]["images"][0]["url"]
        releaseDate = track["track"]["album"]["release_date"]
        uri = track["track"]["uri"]

        tracks.append(
            {
                "Id Track": idTrack,
                "Album Name": albumName,
                "Track Name": trackName,
                "Artist Name": artistsName,
                "Duration in ms": durationMs,
                "Popularity": popularity,
                "Album imagen": albumImage,
                "Release date": releaseDate,
                "uri": uri
            }
        )

    return tracks


def getAudioFeatures(spotifyAuth, ids):
    audioFeatures = []
    print("\n..Obteniendo Features..\n")
    while ids:
        audioFeatures += spotifyAuth.audio_features(ids[:100])
        print(f"faltan {len(ids)} items por evaluar ...")
        ids = ids[100:]
    print("Consulta completa\n")
    return audioFeatures
