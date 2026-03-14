"""Basic example — connect to a TikTok LIVE stream and print all events.

Usage:
    # Set environment variables first:
    # Linux/macOS:  export TIKTOOL_API_KEY=your_key  TIKTOK_USERNAME=streamer
    # Windows CMD:  set TIKTOOL_API_KEY=your_key  & set TIKTOK_USERNAME=streamer
    # PowerShell:   $env:TIKTOOL_API_KEY="your_key"; $env:TIKTOK_USERNAME="streamer"

    python basic.py
"""

import os
import sys

from tiktok_live_api import TikTokLive

USERNAME = os.environ.get("TIKTOK_USERNAME", "")
if not USERNAME:
    print("Set TIKTOK_USERNAME environment variable to the streamer's username.")
    sys.exit(1)

client = TikTokLive(USERNAME)


@client.on("connected")
def on_connected(event):
    print(f"Connected to @{event['uniqueId']}")


@client.on("chat")
def on_chat(event):
    print(f"[chat] {event['user']['uniqueId']}: {event['comment']}")


@client.on("gift")
def on_gift(event):
    diamonds = event.get("diamondCount", 0)
    print(f"[gift] {event['user']['uniqueId']} sent {event['giftName']} ({diamonds} diamonds)")


@client.on("like")
def on_like(event):
    print(f"[like] {event['user']['uniqueId']} liked (total: {event['totalLikes']})")


@client.on("follow")
def on_follow(event):
    print(f"[follow] {event['user']['uniqueId']} followed")


@client.on("roomUserSeq")
def on_viewers(event):
    print(f"[viewers] {event['viewerCount']} watching")


@client.on("streamEnd")
def on_stream_end(event):
    print("[stream] Stream has ended.")


client.run()
