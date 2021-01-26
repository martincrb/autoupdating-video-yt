#!/usr/bin/python
# -*- coding: latin-1 -*-

import httplib2
import os
import sys

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('miniatura.png')
#texted_image = putText(img=np.copy(image), text='Test', org=(200, 200),
#        fontFace=3, fontScale=3, color=(0,0,255), thickness=5)

CLIENT_SECRETS_FILE = "client_id.json"
MISSING_CLIENT_SECRETS_MESSAGE = "Missing client secrets"
YOUTUBE_READWRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  redirect_uri="urn:ietf:wg:oauth:2.0:oob",
  scope=YOUTUBE_READWRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

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
  video_id="YOUR_VIDEO_ID_HERE"
  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_response = youtube.videos().list(
    id=video_id,
    part="snippet, statistics",
  ).execute()
  statistics = playlistitems_list_response["items"][0]["statistics"]
  snippet = playlistitems_list_response["items"][0]["snippet"]
  snippet["title"] = "Este vídeo tiene " + str(statistics["viewCount"])+" visitas y se ACTUALIZA. ¡Te ENSEÑO como hacerlo!"
  cv2.putText(image, str(statistics["viewCount"]), (183, 300),
          cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 15)
  cv2.imwrite('miniatura-output.png', image)
  print snippet["title"]
  youtube.videos().update(part="snippet",body=dict(snippet=snippet, id=video_id)).execute()
  youtube.thumbnails().set(videoId=video_id, media_body='miniatura-output.png').execute()
