#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
from apiclient.discovery import build
import google.auth
import google.oauth2.credentials

import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('miniatura.png')

REFRESH_TOKEN=os.environ['REFRESH_TOKEN']
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
CLIENT_ID=os.environ['CLIENT_ID']
TOKEN_URI=os.environ['TOKEN_URI']
CLIENT_SECRET=os.environ['CLIENT_SECRET']
YOUTUBE_VIDEO_ID = os.environ['YOUTUBE_VIDEO_ID']

MISSING_CLIENT_SECRETS_MESSAGE = "Missing client secrets"
YOUTUBE_READWRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


credentials = google.oauth2.credentials.Credentials(
  ACCESS_TOKEN,
  refresh_token=REFRESH_TOKEN,
  client_id=CLIENT_ID,
  token_uri=TOKEN_URI,
  client_secret=CLIENT_SECRET)


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

# Retrieve the contentDetails part of the channel resource for the
# authenticated user's channel.
channels_response = youtube.channels().list(
  mine=True,
  part="contentDetails"
).execute()

for channel in channels_response["items"]:
  # From the API response, extract the playlist ID that identifies the list
  # of videos uploaded to the authenticated user's channel.
  uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
  video_id = YOUTUBE_VIDEO_ID
  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_response = youtube.videos().list(
    id=video_id,
    part="snippet, statistics",
  ).execute()
  statistics = playlistitems_list_response["items"][0]["statistics"]
  print(statistics)
  snippet = playlistitems_list_response["items"][0]["snippet"]
  snippet["title"] = "Este video tiene " + str(statistics["viewCount"])+" visitas y " +str(statistics["dislikeCount"])+ " dislikes... Te MUESTRO como hacerlo!"
  cv2.putText(image, str(statistics["viewCount"]), (183, 300),
          cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 15)
  cv2.imwrite('miniatura-output.png', image)
  print(snippet["title"])
  youtube.videos().update(part="snippet",body=dict(snippet=snippet, id=video_id)).execute()
  youtube.thumbnails().set(videoId=video_id, media_body='miniatura-output.png').execute()
