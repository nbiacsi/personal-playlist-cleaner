# Overview
Script developed in Python that is run as a Linux service as the local user on startup of the system to get all IDs of all Liked Songs and IDs of all songs in another workout playlist in Spotify. Once received, the script will loop through all songs in the playlist and check if each song is a liked song. If any songs are found to not be a liked song, that song gets removed from the workout playlist.

# Prerequisites
Python, uv and the Python modules listed in pyproject.toml and uv.lock need to be installed. A Spotify application also needs to be set up on the Spotify Developer portal: https://developer.spotify.com. Once created, copy your access key and secret access keys as these will be used in the script.

# Setup
## Project Setup
Clone this project by typing this command in the terminal: `git clone https://github.com/nbiacsi/personal-playlist-cleaner.git`

Once complete, navigate to the project directory by typing this command in the terminal: `cd personal-playlist-cleaner`

Once there, create the virtual environment and install the modules with this command: `uv sync`

This will install the modules listed in pyproject.toml and uv.lock within a newly created virtual environment.

## Environment Variables
One of the modules that were installed is called python-dotenv. This module is used to store environment variables like the Access Key and Secret Access Keys Spotify gave us when setting up the project. To use this module, create a file in the project directory called `.env` and open the file in a text editor and set up the file as shown below:
```
CLIENT_ID="your spotify access key"
CLIENT_SECRET="your spotify secret access key"
REDIRECT_URI="your spotify redirect uri"
USERNAME="your spotify username"
```

These keys are only used in the authorize function where you see they are loaded with the `os.getenv("Name-of-key")` function call. Make sure to replace the values with your own keys in the `.env` file.

**Note:** If you have the ID of the playlist you want to clean, you can set it as an environment variable called `PLAYLIST_ID` in the `.env` file.

# Execution of Script
## Manual
If you want to run the script manually, run this command in the terminal: `uv run main.py`

**Note:** You will need to run this script manually before deploying it as a service as you will need to authorize the user/device in a browser with Spotify. Once you do that, you should be able to run this script as a service/job.

## Auto-Logon Service
If you want to run the script automatically as a service on boot, you will need to follow the below steps.

Create a new service file (it doesn't matter how it's named) in this location `/etc/systemd/system`. It will need these file contents:
```
[Unit]
Description=Spotify Playlist Cleaner script
After=multi-user.target

[Service]
Type=simple
User=sloth
Group=sloth
ExecStart=/opt/playlist_cleaner.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Where the `sloth` user and group is the user that will run the script. Replace those with the name of the local user that will run the script.

Edit the `playlist_cleaner.sh` file to include the correct path to the `playlist_cleaner.py` file that's set up on your system.

Copy the `playlist_cleaner.sh` file to `/opt` and make it executable with this command: `sudo cp playlist_cleaner.sh /opt && sudo chmod +x /opt/playlist_cleaner.sh`

Enable the service with this command: `sudo systemctl enable playlist_cleaner.service`

Start the service with this command: `sudo systemctl start playlist_cleaner.service`

If the service shows as running and everything is working correctly, then you know the service is working correctly and will run again upon each boot of the system.
