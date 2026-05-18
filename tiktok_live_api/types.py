"""Type definitions for TikTok LIVE API events.

These types can be used for IDE autocompletion and type checking
when handling events from :class:`~tiktok_live_api.TikTokLive` and
:class:`~tiktok_live_api.TikTokCaptions`.
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = [
    "TikTokUser",
    "ChatEvent",
    "GiftEvent",
    "LikeEvent",
    "MemberEvent",
    "SocialEvent",
    "RoomUserSeqEvent",
    "BattleEvent",
    "BattleArmiesEvent",
    "BattleItemCardEvent",
    "BattleHost",
    "BattleContributor",
    "RoomPinEvent",
    "CaptionEvent",
    "TranslationEvent",
]


class TikTokUser(TypedDict, total=False):
    """User profile attached to most LIVE events."""

    userId: str
    uniqueId: str
    nickname: str
    profilePictureUrl: str
    followRole: int
    isSubscriber: bool


class ChatEvent(TypedDict, total=False):
    """Payload for ``chat`` events."""

    user: TikTokUser
    comment: str
    emotes: List[Dict[str, Any]]
    starred: Dict[str, int]  # {"claps": N, "score": N} — present only for starred messages


class GiftEvent(TypedDict, total=False):
    """Payload for ``gift`` events."""

    user: TikTokUser
    giftId: int
    giftName: str
    diamondCount: int
    repeatCount: int
    repeatEnd: bool


class LikeEvent(TypedDict, total=False):
    """Payload for ``like`` events."""

    user: TikTokUser
    likeCount: int
    totalLikes: int


class MemberEvent(TypedDict, total=False):
    """Payload for ``member`` (viewer join) events."""

    user: TikTokUser
    actionId: int


class SocialEvent(TypedDict, total=False):
    """Payload for ``follow`` and ``share`` events."""

    user: TikTokUser
    eventType: str


class RoomUserSeqEvent(TypedDict, total=False):
    """Payload for ``roomUserSeq`` (viewer count) events."""

    viewerCount: int
    topViewers: List[TikTokUser]


class BattleEvent(TypedDict, total=False):
    """Payload for ``battle`` events (PK start / end / countdown)."""

    type: str
    battleId: str
    status: int
    """1=ACTIVE, 2=STARTING, 3=ENDED, 4=PREPARING"""
    battleDuration: int
    teams: List[Dict[str, Any]]
    scores: List[int]


class BattleContributor(TypedDict, total=False):
    """One contributor (gifter) on a battle host's side."""

    userId: str
    score: int
    nickname: str


class BattleHost(TypedDict, total=False):
    """One host on a battle side — multi-guest PK breakdown."""

    hostUserId: str
    teamTotalScore: int
    teamIdx: int
    contributors: List[BattleContributor]
    """Sorted MVP first (highest score → lowest)."""


class BattleArmiesEvent(TypedDict, total=False):
    """Payload for ``battleArmies`` events — score updates during PK."""

    battleId: str
    status: int
    teams: List[Dict[str, Any]]
    matchId: str
    """Stable across multi-round PK."""
    sessionId: str
    """Per-round session id."""
    startedAtMs: int
    serverTsMs: int
    sessionTag: str
    durationSec: int
    secsRemaining: int
    """Countdown: duration − (serverTs − startedAt)."""
    hosts: List[BattleHost]


class BattleItemCardEvent(TypedDict, total=False):
    """Payload for ``battleItemCard`` events — booster multipliers, gloves, mist, etc."""

    battleId: str
    cardType: int
    """2=gloves/crit, 3=mist, 4=match_guide, ..."""
    effect: str
    """'gloves' | 'mist' | 'booster_x2' | 'booster_x3' | 'match_guide' | 'thunder' | 'extra_time' | raw key."""
    effectKey: str
    multiplier: int
    """2 or 3 for booster_x2/x3, otherwise 0."""
    senderUserId: str
    senderNickname: str
    senderUniqueId: str
    activatedAtSec: int
    durationSec: int
    endsAtSec: int
    commentTemplate: str


class RoomPinEvent(TypedDict, total=False):
    """Payload for ``roomPin`` (starred/pinned message) events.

    Fired when a host or moderator pins a chat message.
    """

    user: TikTokUser
    """User who wrote the pinned message."""
    comment: str
    """The pinned comment text."""
    action: int
    """Pin action: 1 = pin, 2 = unpin."""
    durationSeconds: int
    """How long the message stays pinned (seconds)."""
    pinnedAt: int
    """Timestamp when the message was pinned (ms)."""
    originalMsgType: str
    """Original message type, e.g. 'WebcastChatMessage'."""
    originalMsgId: str
    """ID of the original chat message that was pinned."""
    operatorUserId: str
    """User ID of the host/moderator who pinned the message."""


class CaptionEvent(TypedDict, total=False):
    """Payload for ``caption`` events from :class:`~tiktok_live_api.TikTokCaptions`."""

    text: str
    speaker: str
    isFinal: bool
    language: str


class TranslationEvent(TypedDict, total=False):
    """Payload for ``translation`` events from :class:`~tiktok_live_api.TikTokCaptions`."""

    text: str
    sourceLanguage: str
    targetLanguage: str
