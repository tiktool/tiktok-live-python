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
    "NativeCaptionEvent",
]


class TikTokUser(TypedDict, total=False):
    """User profile attached to most LIVE events."""

    userId: str
    uniqueId: str
    nickname: str
    profilePictureUrl: str
    followRole: int
    isSubscriber: bool
    # TikTok donator / spender level (1 to 50). Present on every user-bearing
    # event (chat / gift / like / follow / member / share) when the user has
    # gifted at least once on the platform. Extracted from the proto badge
    # category 20 sub category 8 priv.level_string. Absent when the user has
    # never gifted. The wire field name on api.tik.tools is `level`; alias
    # `payGrade` matches the @tiktool/live JS SDK shape for cross-language
    # consumers.
    level: int
    payGrade: int


class ChatEvent(TypedDict, total=False):
    """Payload for ``chat`` events."""

    user: TikTokUser
    comment: str
    emotes: List[Dict[str, Any]]
    starred: Dict[str, int]  # {"claps": N, "score": N} - present only for starred messages
    # v3 (2026-06-07): TikTok auto-detected language (ISO 639-1, "un" = unknown)
    language: str
    # v3 (2026-06-07): stable per-message UUID used by chat-delete / moderation events
    messageUuid: str
    # Proto schema version this event was decoded against (1, 2, or 3).
    # See https://tik.tools/docs for the migration matrix; v3-only fields are
    # surfaced only when present so legacy v1/v2 callers can keep ignoring them.
    protoVersion: int


class GiftEvent(TypedDict, total=False):
    """Payload for ``gift`` events."""

    user: TikTokUser
    giftId: int
    giftName: str
    diamondCount: int
    repeatCount: int
    repeatEnd: bool
    # v3 (2026-06-07): stable per-gift transaction id (hex string) - dedup key.
    transactionId: str
    # v3 (2026-06-07): explicit sender id (mirrors user.id but TikTok ships
    # it separately on the wire so we surface it for safe comparison).
    senderUserId: str
    # v3 (2026-06-07): relationship metadata when TikTok attaches it.
    # Shape: { joinDayNumber: int, fromUser: str, toUser: str }
    relationship: Dict[str, Any]
    protoVersion: int


class LikeEvent(TypedDict, total=False):
    """Payload for ``like`` events."""

    user: TikTokUser
    likeCount: int
    totalLikes: int


class MemberEvent(TypedDict, total=False):
    """Payload for ``member`` (viewer join) events."""

    user: TikTokUser
    actionId: int
    # v3 (2026-06-07): granular subcode (38, 44, ...) finer than actionId.
    actionCode: int
    # v3 (2026-06-07): where the viewer came from -
    # "homepage_hot-live_cell", "follow-tab", ...
    entrySource: str
    # v3 (2026-06-07): how the viewer entered -
    # "draw" (algorithmic surface), "click" (explicit), "other".
    entryAction: str
    # v3 (2026-06-07): "rec" when TikTok recommended this stream to the viewer.
    entryType: str
    protoVersion: int


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
    """One host on a battle side - multi-guest PK breakdown."""

    hostUserId: str
    teamTotalScore: int
    teamIdx: int
    contributors: List[BattleContributor]
    """Sorted MVP first (highest score → lowest)."""


class BattleArmiesEvent(TypedDict, total=False):
    """Payload for ``battleArmies`` events - score updates during PK."""

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
    """Payload for ``battleItemCard`` events - booster multipliers, gloves, mist, etc."""

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
    senderAvatarUrl: str
    activatedAtSec: int
    durationSec: int
    endsAtSec: int
    commentTemplate: str
    iconUrl: str
    """Full TikTok CDN URL for the card art."""
    iconKey: str
    """Short identifier - ``card_mist_v3``, ``card_crit_v3``, ``top3_buffer``, ..."""
    accentColor: str
    """Hex accent color (``#BCD9E0`` mist, ``#E0D4BC`` gloves, ...)."""


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


class NativeCaptionEvent(TypedDict, total=False):
    """Payload for ``caption`` events from :class:`~tiktok_live_api.TikTokLive`.

    v3 (2026-06-07): TikTok now ships native auto-captions directly on the
    LIVE WebSocket via ``WebcastCaptionMessage``. Each frame carries one
    caption window with text, start/end timestamps, and an ``isFinal`` flag.
    Independent of the operator-managed :class:`TikTokCaptions` product -
    this is what TikTok's own viewer UI renders for accessibility / Discover.
    """

    text: str
    isFinal: bool
    startedAtMs: int
    endsAtMs: int
    protoVersion: int
