# Overview
Script developed in Python that is run on a Windows Task Scheduler weekly to get all IDs of all Liked Songs and IDs of all songs in my workout playlist in Spotify. Once received, the script will loop through all songs in my playlist and check if the song is in the Liked Songs playlist. If any songs are found to not be in that playlist, that song gets removed from the workout playlist.

# Prerequisites
Python and the Python module listed in requirements.txt need to be installed. A Spotify application also needs to be set up on the Spotify Developer portal: https://developer.spotify.com. Once created, copy your access key and secret access keys as these will be used in the script.

# Setup

## Virtual Environment Setup
A virtual environment is a containerized environment for a given Python project. The main benefit of a virtual environment set up like this is you can install all of the Python modules required for a project to work in the virtual environment which is independent of the rest of the modules installed outside of the virtual environment. To create a virtual environment, create a new folder locally on your system where this Python script and project will live. Copy the file into that directory along with the requirements.txt file which will be used in the next step. Open the terminal on your computer and go to that directory. Once there, type in this command to create a new virtual environment for this Python project: 
***python -m venv .venv***

Once you see the command line come back, and the folder called **.venv** is created, you can move onto the next step.

## Module Install
Included in this project is a requirements.txt file. This file is used to install the modules required for this script to run. Before installing the modules, we'll need to activate the virtual environment. To do that, while having the terminal open in the project directory, if you're on Windows type this command:
***.venv\Scripts\activate***

Or if you're on Linux or MacOS type this command:
***source .venv/bin/activate***

If you see a **(.venv)** in front of the terminal then you know it's working.

To install the modules, type in this command:
***pip install -r requirements.txt***

This command will install all modules in the requirements.txt folder that are required for this project to run. Once you can interact with the terminal again, that means the modules are all installed.

## Environment Variables
One of the modules that were installed is called python-dotenv. This module is used to store environment variables like the Access Key and Secret Access Keys Spotify gave us when setting up the project. To use this module, create a file in the project directory called **.env** and open the file in a text editor and set up the file as shown below:
***ACCESS_KEY="your spotify access key"
SECRET_KEY="your spotify secret access key"***

These keys are only used in the authorize function where you see they are loaded with the **os.getenv("Name-of-key")**

# Execution of Script
Whenever this script is executed, make sure this script is run with the virtual environment loaded whether the script is being executed by yourself or through an automated means, say on a Task Scheduler job, for example. If you are executing the script through automated means, you can create a .bat file to execute the virtual environment and then script right after. Here's an example of how the .bat file contents could look like:
***"path/to/.venv" && python "path/to/script.py"***

Once the batch file is created, call it as the executable and it will work.
