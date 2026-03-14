"""Live Captions example — transcribe and translate a TikTok LIVE stream.

Usage:
    # Set environment variables first:
    # Linux/macOS:  export TIKTOOL_API_KEY=your_key  TIKTOK_USERNAME=streamer
    # Windows CMD:  set TIKTOOL_API_KEY=your_key  & set TIKTOK_USERNAME=streamer
    # PowerShell:   $env:TIKTOOL_API_KEY="your_key"; $env:TIKTOK_USERNAME="streamer"

    python captions.py
"""

import os
import sys

from tiktok_live_api import TikTokCaptions

USERNAME = os.environ.get("TIKTOK_USERNAME", "")
if not USERNAME:
    print("Set TIKTOK_USERNAME environment variable to the streamer's username.")
    sys.exit(1)

captions = TikTokCaptions(
    USERNAME,
    translate="en",
    diarization=True,
)


@captions.on("connected")
def on_connected(event):
    print(f"Listening to @{event['uniqueId']}")


@captions.on("caption")
def on_caption(event):
    speaker = event.get("speaker", "")
    text = event["text"]
    is_final = event.get("isFinal", False)
    status = "FINAL" if is_final else "partial"
    print(f"[{status}] [{speaker}] {text}")


@captions.on("translation")
def on_translation(event):
    print(f"  -> {event['text']}")


captions.run()
