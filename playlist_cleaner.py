'''
    Author: Sloth
    Date: 9/16/2024
    Description: Python script to get all songs in Hype playlist and remove all songs that aren't liked songs.
'''

from dotenv import load_dotenv
import spotipy
import spotipy.util as util

import os
from typing import Any


load_dotenv()


def remove_songs(sp: spotipy.Spotify, liked_songs: list[str], playlist_songs: list[str], playlist_id: str) -> None:
    '''
    Removes songs that are in the Hype playlist that are not liked songs.

    Args:
        sp (spotipy.Spotify): Spotipy authentication object.
        liked_songs (list[str]): List of liked song IDs.
        playlist_songs (list[str]): List of Hype song IDs.
        playlist_id (str): ID of the Hype playlist.

    Returns:
        None.
    '''

    songs: list[str] = [song for song in playlist_songs if song not in liked_songs]
    if len(songs) > 0:
        sp.playlist_remove_all_occurrences_of_items(
            playlist_id, songs, snapshot_id=None
        )


def get_hypesongs(sp: spotipy.Spotify, playlist_id: str) -> list[str]:
    '''
    Gets IDs of all Hype playlist songs.

    Args:
        sp (spotipy.Spotify): Spotipy authentication object.
        playlist_id (str): ID of the Hype playlist.

    Returns:
        list[str]: Hype song IDs.
    '''

    songs: list[str] = []
    i: int = 0
    while True:
        if i == 0:
            response = sp.playlist_tracks(playlist_id)
        else:
            response = sp.next(response)

        for song in response['items']:
            songs.append(song['track']['id'])

        if response['next'] == None:
            return songs

        i += 1


def get_likedsongs_response(sp: spotipy.Spotify, liked_songs_count: int) -> dict[str, Any]:
    '''
    Gets the total response object of all liked songs.

    Args:
        sp (spotipy.Spotify): Spotipy authentication object.
        liked_songs_count (int): Count of liked songs.

    Returns:
        dict[str, Any]: Response object of all liked songs.
    '''

    response: dict[str, str] = {}
    i: int = 0
    limit: int = 50
    while i < liked_songs_count:
        offset: int = i + 50
        if offset > liked_songs_count:
            limit = offset - liked_songs_count

        results = sp.current_user_saved_tracks(offset=i, limit=limit)
        response[i] = results
        i += 50

    return response


def get_likedsongs(sp: spotipy.Spotify) -> list[str]:
    '''
    Gets all IDs of liked songs.

    Args:
        sp (spotipy.Spotify): Spotipy authentication object.

    Returns:
        list[str]: Liked song IDs
    '''

    liked_songs_count = sp.current_user_saved_tracks()['total']
    response: dict[str, str] = get_likedsongs_response(sp, liked_songs_count)
    liked_songs: list[str] = []
    i: int = 0
    blob: int = 0

    while i < liked_songs_count and blob < liked_songs_count:
        songs: list[dict[str, str]] = response[blob]['items']
        for j in range(len(songs)):
            liked_songs.append(songs[j]['track']['id'])
            i += 1

        blob += 50

    return liked_songs


def get_playlist_id(sp: spotipy.Spotify) -> str:
    '''
    Gets the Hype playlist ID to remove songs from.

    Args:
        sp (spotipy.Spotify): Spotipy authentication object.

    Returns:
        str: Hype playlist ID.
    '''

    id: str = sp.me()['id']
    return sp.user_playlists(id)['items'][0]['id']


def authorize() -> spotipy.Spotify:
    '''
    Gets a spotipy.Spotify authentication object used to make calls to the spotipy module.

    Args:
        None.

    Returns:
        spotipy.Spotify: Spotipy authentication object.
    '''

    client_id: str = os.getenv('CLIENT_ID')
    client_secret: str = os.getenv('CLIENT_SECRET')
    redirect_uri: str = 'http://localhost:7777/callback'
    scope: str = 'user-library-read playlist-modify-public'
    username: str = 'nickbiacsi@gmail.com'

    token: str = util.prompt_for_user_token(
        username,
        scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    return spotipy.Spotify(auth=token)


def main() -> None:
    sp = authorize()
    playlist_id: str = get_playlist_id(sp)
    liked_songs: list[str] = get_likedsongs(sp)
    hype_songs: list[str] = get_hypesongs(sp, playlist_id)
    remove_songs(sp, liked_songs, hype_songs, playlist_id)


if __name__ == '__main__':
    main()
