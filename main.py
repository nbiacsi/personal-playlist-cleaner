'''
    Author: Sloth
    Date: 3/19/2026
    Description: FastAPI server to host data from Spotify API to be used to clean Spotify Hype playlist.
'''

from fastapi import FastAPI

app = FastAPI()


@app.get('/liked')
def get_liked_songs() -> dict[str, list[str]]:
    return {'Liked Songs': ['Song A', 'Song B', 'Song C']}


@app.get('/playlist/{playlist_id}')
def get_playlist_songs(playlist_id: str) -> dict[str, list[str]]:
    return {'Playlist Songs': ['Song X', 'Song Y', 'Song Z']}


@app.post('/playlist/{playlist_id}')
def remove_playlist_songs(playlist_id: str, songs: list[str]) -> dict[str, str]:
    return {'Removed': 'Playlist Songs'}
