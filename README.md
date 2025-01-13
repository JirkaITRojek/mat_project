# Mat Project Setup Guide

This guide will walk you through the steps to set up the Mat Project locally on your machine. Follow the steps below to get everything running.

##Clone the Repository

First, clone the repository to your local machine:

```bash
git clone -b master https://github.com/JirkaITRojek/mat_project
```
```bash
cd mat_project
```
##Set Up a Virtual Environment
```bash
python -m venv .env
.env\Scripts\activate
```
##Create a secret.py File
```bash
At the same level as main.py, create a file named secret.py and add the following content:
BOT_TOKEN = "MTI4Nzc2NTg2MDI5OTMwOTExOA.GHfYkJ.mZ3B2qF9sG8Kv5n4rZ-uTq0qPtwEdvkwqIhsZA"
REDDIT_CLIENT_ID = "abcdefg1234567hijklmn89opqrst"
REDDIT_CLIENT_SECRET = "abcdefg1234567hijklmn89opqrst"
```
##Install Dependencies
```bash
Now, install the required Python packages using pip:
pip install -r requirements.txt
```
##Install FFmpeg
```bash
Download FFmpeg from the official website: FFmpeg Download
Windows Users: Make sure to download the Windows build and extract the zip file.
After downloading, place the ffmpeg.exe file in a folder (e.g., C:\ffmpeg\bin\ffmpeg.exe).
```
##Configure FFmpeg in settings.py
```bash
Open the settings.py file in the project and set the FFMPEG_PATH to the path where you placed the ffmpeg.exe file. For example:
FFMPEG_PATH = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
```
##Run the Project
```bash
py main.py runserver
```

