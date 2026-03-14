"""Chat bot example — respond to commands and track a gift leaderboard.

Usage:
    # Set environment variables first:
    # Linux/macOS:  export TIKTOOL_API_KEY=your_key  TIKTOK_USERNAME=streamer
    # Windows CMD:  set TIKTOOL_API_KEY=your_key  & set TIKTOK_USERNAME=streamer
    # PowerShell:   $env:TIKTOOL_API_KEY="your_key"; $env:TIKTOK_USERNAME="streamer"

    python chat_bot.py
"""

import os
import sys
from typing import Dict

from tiktok_live_api import TikTokLive

USERNAME = os.environ.get("TIKTOK_USERNAME", "")
if not USERNAME:
    print("Set TIKTOK_USERNAME environment variable to the streamer's username.")
    sys.exit(1)

client = TikTokLive(USERNAME)

gift_leaderboard: Dict[str, int] = {}
message_count = 0


@client.on("chat")
def on_chat(event):
    global message_count
    message_count += 1
    msg = event["comment"].lower().strip()
    user = event["user"]["uniqueId"]

    if msg == "!hello":
        print(f">> BOT: Welcome {user}!")
    elif msg == "!stats":
        print(f">> BOT: {message_count} messages, {len(gift_leaderboard)} gifters")
    elif msg == "!top":
        top = sorted(gift_leaderboard.items(), key=lambda x: -x[1])[:5]
        for rank, (name, diamonds) in enumerate(top, start=1):
            print(f"  {rank}. {name} - {diamonds} diamonds")


@client.on("gift")
def on_gift(event):
    user = event["user"]["uniqueId"]
    diamonds = event.get("diamondCount", 0)
    gift_leaderboard[user] = gift_leaderboard.get(user, 0) + diamonds
    print(f"[gift] {user} sent {event['giftName']} ({diamonds} diamonds)")


client.run()
