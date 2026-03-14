"""TikTok Live API — TikTok LIVE stream data client for Python.

Connect to any TikTok LIVE stream and receive real-time events:
chat messages, gifts, likes, follows, viewer counts, battles, and more.

Usage::

    from tiktok_live_api import TikTokLive

    client = TikTokLive("streamer_username", api_key="YOUR_KEY")

    @client.on("chat")
    def on_chat(event):
        print(f"{event['user']['uniqueId']}: {event['comment']}")

    client.run()

See https://tik.tools/docs for full documentation.
"""

from tiktok_live_api.client import TikTokLive
from tiktok_live_api.captions import TikTokCaptions
from tiktok_live_api.types import (
    TikTokUser,
    ChatEvent,
    GiftEvent,
    LikeEvent,
    MemberEvent,
    SocialEvent,
    RoomUserSeqEvent,
    BattleEvent,
    CaptionEvent,
    TranslationEvent,
)

__all__ = [
    "TikTokLive",
    "TikTokCaptions",
    "TikTokUser",
    "ChatEvent",
    "GiftEvent",
    "LikeEvent",
    "MemberEvent",
    "SocialEvent",
    "RoomUserSeqEvent",
    "BattleEvent",
    "CaptionEvent",
    "TranslationEvent",
]
__version__ = "1.0.1"
