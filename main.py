'''
    Author: Sloth
    Date: 9/16/2024
    Description: Python script remove all songs from a playlist that are not liked songs.
'''

from dotenv import load_dotenv
import spotipy
from spotipy import Spotify

from dataclasses import dataclass
import os
import time
from typing import Any

load_dotenv(override=True)

PAGE_SIZE: int = 50
SCOPE: str = 'user-library-read playlist-modify-public'


@dataclass(frozen=True)
class PlaylistConfig:
    sp: Spotify
    playlist_id: str


def remove_songs(playlist_config: PlaylistConfig, songs_to_remove: set[str], remove_count: int) -> None:
    '''
    Removes songs that are in the Hype playlist that are not liked songs.

    Args:
        playlist_config (PlaylistConfig): Playlist configuration object.
        songs_to_remove (set[str]): Set of song IDs to remove from the playlist.
        remove_count (int): Number of songs to remove.

    Returns:
        None.
    '''


    REMOVE_LIMIT: int = 100
    if remove_count <= REMOVE_LIMIT:
        playlist_config.sp.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist_config.playlist_id,
            items=list(songs_to_remove)
        )

    start: int = 0
    while remove_count > 0:
        if remove_count < REMOVE_LIMIT:
            end: int = start + remove_count
        else:
            end = start + REMOVE_LIMIT

        playlist_config.sp.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist_config.playlist_id,
            items=list(songs_to_remove)[start:end]
        )
        remove_count -= REMOVE_LIMIT
        start += REMOVE_LIMIT


def get_playlist_songs(playlist_config: PlaylistConfig) -> set[str]:
    '''
    Gets IDs of all songs in the playlist.

    Args:
        playlist_config (PlaylistConfig): Playlist configuration object.

    Returns:
        set[str]: List of song IDs from the playlist.
    '''

    playlist_songs: set[str] = set()
    response = playlist_config.sp.playlist_tracks(playlist_config.playlist_id)
    next: bool = True
    while next:
        for song in response['items']:  # pyright: ignore[reportOptionalSubscript]
            playlist_songs.add(song['track']['id'])

        if response['next'] is not None:  # pyright: ignore[reportOptionalSubscript]
            response = playlist_config.sp.next(response)
            continue

        next = False

    return playlist_songs


def get_liked_songs_response(sp: Spotify, liked_songs_count: int) -> dict[Any, Any]:
    '''
    Gets the total response object of all liked songs.

    Args:
        sp (Spotify): Spotipy authentication object.
        liked_songs_count (int): Count of liked songs.

    Returns:
        dict[Any, Any]: Response object of all liked songs.
    '''

    response: dict[Any, Any] = {}
    i, limit = 0, 50
    while i < liked_songs_count:
        offset: int = i + PAGE_SIZE
        if offset > liked_songs_count:
            limit = offset - liked_songs_count

        response[i] = sp.current_user_saved_tracks(offset=i, limit=limit)
        i += PAGE_SIZE

    return response


def get_liked_songs(sp: Spotify) -> set[str]:
    '''
    Gets all IDs of liked songs.

    Args:
        sp (Spotify): Spotipy authentication object.

    Returns:
        set[str]: Liked song IDs
    '''

    liked_songs_count: int = sp.current_user_saved_tracks()['total']  # pyright: ignore[reportOptionalSubscript]
    response: dict[Any, Any] = get_liked_songs_response(sp, liked_songs_count)
    liked_songs: set[str] = set()

    i, blob = 0, 0
    while i < liked_songs_count and blob < liked_songs_count:
        songs: list[dict[str, Any]] = response[blob]['items']
        for j in range(len(songs)):
            liked_songs.add(songs[j]['track']['id'])
            i += 1

        blob += PAGE_SIZE

    return liked_songs


def get_playlist_id(sp: Spotify) -> str:
    '''
    Gets the Hype playlist ID to remove songs from.

    Args:
        sp (Spotify): Spotipy authentication object.

    Returns:
        str: Playlist ID.
    '''

    id: str = sp.me()['id']  # pyright: ignore[reportOptionalSubscript]
    return sp.user_playlists(id)['items'][0]['id']  # pyright: ignore[reportOptionalSubscript]


def authorize() -> Spotify:
    '''
    Gets a Spotify authentication object used to make calls to the spotipy module.

    Args:
        None.

    Returns:
        Spotify: Spotipy authentication object.
    '''

    client_id: str | None = os.getenv('CLIENT_ID')
    client_secret: str | None = os.getenv('CLIENT_SECRET')
    redirect_uri: str | None = os.getenv('REDIRECT_URI')
    username: str | None = os.getenv('USERNAME')

    if any([client_id is None, client_secret is None, redirect_uri is None, username is None]):
        raise Exception('Missing environment variables')

    token = spotipy.util.prompt_for_user_token(
        username=username,
        scope=SCOPE,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    return Spotify(auth=token)


def main() -> None:
    sp: Spotify = authorize()

    # Wait for a minute to start up the system to ensure it runs without error.
    time.sleep(60)
    playlist_id: str | None = os.getenv('PLAYLIST_ID')
    if playlist_id is None:
        playlist_id = get_playlist_id(sp)

    liked_songs: set[str] = get_liked_songs(sp)

    playlist_config: PlaylistConfig = PlaylistConfig(sp, playlist_id)
    playlist_songs: set[str] = get_playlist_songs(playlist_config)
    songs_to_remove: set[str] = playlist_songs.difference(liked_songs)

    remove_count = len(songs_to_remove)
    if remove_count > 0:
        remove_songs(playlist_config, songs_to_remove, remove_count)

if __name__ == '__main__':
    main()
