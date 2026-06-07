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
    # v3 (2026-06-07) - Tier 2 / Tier 3 additions
    "LinkMicOpponentGiftEvent",
    "ImDeleteEvent",
    "GoalUpdateEvent",
    "PrivilegeAdvanceEvent",
    "CommentTrayEvent",
    "LinkLayerEvent",
    "LinkMessageEvent",
    "GiftPanelUpdateEvent",
    "GameServerFeatureEvent",
    "AnchorToolModificationEvent",
    "ShareRevenueNoticeEvent",
    "ViewerPicksUpdateEvent",
    "FanTicketEvent",
    # v3 (2026-06-07) - Tier 4 additions
    "GiftDynamicRestrictionEvent",
    "InRoomBannerEvent",
    "BattlePunishFinishEvent",
    "BattleNoticeEvent",
    "HostBoardEvent",
    "PollEvent",
    "CompetitionEvent",
    "StreamStatusEvent",
    "BattleGameplayEvent",
    "AISummaryEvent",
    "GiftGalleryEvent",
    "CohostLayoutUpdateEvent",
    "FansEventEvent",
    "LinkScreenChangeEvent",
    "RoomStickerEvent",
    "BottomMessageEvent",
    "OecLiveShoppingEvent",
    "RankTextEvent",
    "AccessRecallEvent",
    "UnauthorizedMemberEvent",
    "GuestShowdownEvent",
    # v3 (2026-06-07) - Tier 5 (long-tail rare methods)
    "HotRoomEvent",
    "EnvelopePortalEvent",
    "GroupLiveMemberNotifyEvent",
    "ShortTouchEvent",
    "LinkMicAnchorGuideEvent",
    "GameMomentEvent",
    "CompetitionContributorEvent",
    "PictionaryUpdateEvent",
    "PictionaryEndEvent",
    "PictionaryExitEvent",
    "OecLiveManagerEvent",
    "OecLiveBillboardEvent",
    "PerceptionEvent",
    "QuestionSelectedEvent",
    "QuestionSlideDownEvent",
    "GiftUnlockEvent",
    "EcShortItemRefreshEvent",
    "CapsuleEvent",
    "RoomVerifyEvent",
    "SMBBoardEvent",
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
    # v3 (2026-06-07): additional host user IDs surfaced on multi-guest
    # battles (host pairs beyond the primary two).
    extraHostUserIds: List[str]
    # v3 (2026-06-07): TikTok layout subtype ("cohost_normal_expand_2", ...)
    layoutSubtype: str
    protoVersion: int


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
    """Countdown: duration - (serverTs - startedAt)."""
    hosts: List[BattleHost]
    # v3 (2026-06-07): stable per-frame transaction UUID (hex). Dedup key.
    transactionId: str
    protoVersion: int


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


# ── v3 (2026-06-07) Tier 2 / Tier 3 additions ────────────────────────


class LinkMicOpponentGiftEvent(TypedDict, total=False):
    """Per-gift breakdown from the OPPONENT side of a PK. v3 (2026-06-07)."""

    senderUserId: str
    opponentRoomId: str
    giftId: int
    giftPictureUrl: str
    startedAtMs: int
    endsAtMs: int
    transactionId: str
    protoVersion: int


class ImDeleteEvent(TypedDict, total=False):
    """Chat moderation delete. Correlate via ChatEvent.messageUuid. v3 (2026-06-07)."""

    deletedMsgId: str
    protoVersion: int


class GoalUpdateEvent(TypedDict, total=False):
    """Stream goal progress (subscriber / gift / watch-time goals). v3 (2026-06-07)."""

    goalKey: str
    creatorUserId: str
    contributionLevel: int
    metadataJson: str
    protoVersion: int


class PrivilegeAdvanceEvent(TypedDict, total=False):
    """Viewer privilege tier-up notification with overlay assets. v3 (2026-06-07)."""

    privilegeKey: str
    action: str
    bgUrls: List[str]
    protoVersion: int


class CommentTrayEvent(TypedDict, total=False):
    """Comment tray state change. v3 (2026-06-07)."""

    trayCount: int
    updatedAtMs: int
    relatedMsgId: str
    protoVersion: int


class LinkLayerEvent(TypedDict, total=False):
    """PK / link-mic negotiation event. v3 (2026-06-07)."""

    action: int
    subAction: int
    sourceType: str
    targetUserId: str
    protoVersion: int


class LinkMessageEvent(TypedDict, total=False):
    """Generic link-mic envelope. v3 (2026-06-07)."""

    action: int
    subAction: int
    relatedUser: TikTokUser
    protoVersion: int


class GiftPanelUpdateEvent(TypedDict, total=False):
    """Real-time gift catalog change for the room. v3 (2026-06-07)."""

    panelId: str
    updatedAtSec: int
    protoVersion: int


class GameServerFeatureEvent(TypedDict, total=False):
    """TikTok Gaming live integration descriptor. v3 (2026-06-07)."""

    rawTag: str
    protoVersion: int


class AnchorToolModificationEvent(TypedDict, total=False):
    """Creator modified a panel / widget on their stream. v3 (2026-06-07)."""

    toolPayload: str
    protoVersion: int


class ShareRevenueNoticeEvent(TypedDict, total=False):
    """Share-revenue subscriber count change notice. v3 (2026-06-07)."""

    creatorUserId: str
    protoVersion: int


class ViewerPicksUpdateEvent(TypedDict, total=False):
    """Viewer-picks gift highlights. v3 (2026-06-07)."""

    pickType: int
    payload: str
    protoVersion: int


class FanTicketEvent(TypedDict, total=False):
    """Fan-ticket method event (fan-club ticket flow). v3 (2026-06-07)."""

    rawPayload: str
    protoVersion: int


# ── v3 Tier 4 (2026-06-07) - 21 lower-volume methods modeled from a
#    30-minute capture across 1963 rooms / 752,955 frames decoded.


class GiftDynamicRestrictionEvent(TypedDict, total=False):
    """Dynamic gift-catalog restriction flip. v3 (2026-06-07)."""

    rawPayload: str
    protoVersion: int


class InRoomBannerEvent(TypedDict, total=False):
    """In-room activity banner carrying a JSON descriptor. v3 (2026-06-07)."""

    activityJson: str
    protoVersion: int


class BattlePunishFinishEvent(TypedDict, total=False):
    """PK punishment phase finished. v3 (2026-06-07)."""

    battleId: str
    punishedUserId: str
    punishType: int
    sessionId: str
    protoVersion: int


class BattleNoticeEvent(TypedDict, total=False):
    """PK notice (version-mismatch toasts, invite-failure messages). v3 (2026-06-07)."""

    noticeCode: int
    noticeKey: str
    noticeText: str
    protoVersion: int


class HostBoardEvent(TypedDict, total=False):
    """Host leaderboard board update. v3 (2026-06-07)."""

    rawPayload: str
    protoVersion: int


class PollEvent(TypedDict, total=False):
    """In-stream poll lifecycle. v3 (2026-06-07)."""

    pollId: str
    action: int
    status: int
    questionPayload: str
    optionsPayload: str
    protoVersion: int


class CompetitionEvent(TypedDict, total=False):
    """Cross-stream competition event. v3 (2026-06-07)."""

    competitionType: int
    layoutSubtype: str
    protoVersion: int


class StreamStatusEvent(TypedDict, total=False):
    """Stream status flip (recording state, content-classification rechecks). v3 (2026-06-07)."""

    rawPayload: str
    protoVersion: int


class BattleGameplayEvent(TypedDict, total=False):
    """PK mini-game gameplay state. v3 (2026-06-07)."""

    gameplayId: str
    gameplayType: int
    subType: int
    protoVersion: int


class AISummaryEvent(TypedDict, total=False):
    """TikTok AI summary of the room. v3 (2026-06-07)."""

    summary: str
    scenarioKey: str
    iconUrl: str
    labelKey: str
    displayDurationMs: int
    protoVersion: int


class GiftGalleryEvent(TypedDict, total=False):
    """Host-side gift wall snapshot. v3 (2026-06-07)."""

    transactionId: str
    protoVersion: int


class CohostLayoutUpdateEvent(TypedDict, total=False):
    """Cohost layout subtype change. v3 (2026-06-07)."""

    layoutSubtype: str
    protoVersion: int


class FansEventEvent(TypedDict, total=False):
    """Fan-club event (tier-up, community refresh). v3 (2026-06-07)."""

    fanType: int
    eventKey: str
    protoVersion: int


class LinkScreenChangeEvent(TypedDict, total=False):
    """PK split-screen layout flip. v3 (2026-06-07)."""

    changeType: int
    sessionInfo: str
    protoVersion: int


class RoomStickerEvent(TypedDict, total=False):
    """Room-wide sticker drop. v3 (2026-06-07)."""

    stickerPayload: str
    protoVersion: int


class BottomMessageEvent(TypedDict, total=False):
    """Bottom-bar safety / risk notice. v3 (2026-06-07)."""

    noticeKey: str
    anchorUserId: str
    durationSec: int
    riskKey: str
    protoVersion: int


class OecLiveShoppingEvent(TypedDict, total=False):
    """OEC live-shopping event (product card display / hide). v3 (2026-06-07)."""

    status: int
    productInfo: str
    protoVersion: int


class RankTextEvent(TypedDict, total=False):
    """Rank text update (top-viewer announcement template). v3 (2026-06-07)."""

    templateKey: str
    userId: str
    protoVersion: int


class AccessRecallEvent(TypedDict, total=False):
    """Access recall (content classification recheck pulls a permission). v3 (2026-06-07)."""

    status: int
    reason: str
    durationSec: int
    suspendKey: str
    protoVersion: int


class UnauthorizedMemberEvent(TypedDict, total=False):
    """Unauthorized member notice (non-logged-in viewer hit a gated feature). v3 (2026-06-07)."""

    templateKey: str
    countLabel: str
    enterToastKey: str
    protoVersion: int


class GuestShowdownEvent(TypedDict, total=False):
    """Guest showdown lifecycle. v3 (2026-06-07)."""

    showdownType: int
    protoVersion: int


# ── v3 Tier 5 (2026-06-07) - long-tail rare methods.


class HotRoomEvent(TypedDict, total=False):
    """Hot-room flag (TikTok promoted the room to a high-traffic slot). v3."""

    hotKey: str
    protoVersion: int


class EnvelopePortalEvent(TypedDict, total=False):
    """Red-envelope portal advance (multi-room envelope chain). v3."""

    sessionInfo: str
    status: int
    kind: int
    level: int
    protoVersion: int


class GroupLiveMemberNotifyEvent(TypedDict, total=False):
    """Group-live member join / leave notify. v3."""

    userId: str
    nickname: str
    protoVersion: int


class ShortTouchEvent(TypedDict, total=False):
    """Short-touch UI (poll, ecommerce lucky bag) state change. v3."""

    variant: str
    action: str
    refId: str
    protoVersion: int


class LinkMicAnchorGuideEvent(TypedDict, total=False):
    """Anchor guide nudges (TikTok prompts the host with a tip). v3."""

    guideCode: int
    rawPayload: str
    protoVersion: int


class GameMomentEvent(TypedDict, total=False):
    """PK / mini-game moment window (highlight clip start / end). v3."""

    momentType: int
    startedAtMs: int
    endsAtMs: int
    momentMsgId: str
    protoVersion: int


class CompetitionContributorEvent(TypedDict, total=False):
    """Per-contributor breakdown inside a cross-stream competition. v3."""

    competitionType: int
    contributorUserId: str
    receiverUserId: str
    protoVersion: int


class PictionaryUpdateEvent(TypedDict, total=False):
    """Drawing-game (Pictionary) round update. v3."""

    status: int
    pictionaryId: str
    protoVersion: int


class PictionaryEndEvent(TypedDict, total=False):
    """Drawing-game round end with revealed answer. v3."""

    pictionaryId: str
    answer: str
    status: int
    protoVersion: int


class PictionaryExitEvent(TypedDict, total=False):
    """Drawing-game exit. v3."""

    pictionaryId: str
    exitReason: int
    protoVersion: int


class OecLiveManagerEvent(TypedDict, total=False):
    """OEC live-manager event (manager assigned / unassigned). v3."""

    status: int
    managerNickname: str
    protoVersion: int


class OecLiveBillboardEvent(TypedDict, total=False):
    """OEC live billboard slot (product wall snapshot). v3."""

    status: int
    slotCount: int
    updatedAtMs: int
    productPayload: str
    flagsPayload: List[str]
    protoVersion: int


class PerceptionEvent(TypedDict, total=False):
    """Perception event (mute cancel etc, TikTok hint signal). v3."""

    perceptionCode: int
    action: str
    protoVersion: int


class QuestionSelectedEvent(TypedDict, total=False):
    """Host picked a viewer-submitted question. v3."""

    questionText: str
    protoVersion: int


class QuestionSlideDownEvent(TypedDict, total=False):
    """Selected-question card slid down (UI dismiss). v3."""

    questionId: str
    protoVersion: int


class GiftUnlockEvent(TypedDict, total=False):
    """Gift-unlock reveal (host unlocked a gated gift). v3."""

    iconUrl: str
    tooltipKey: str
    protoVersion: int


class EcShortItemRefreshEvent(TypedDict, total=False):
    """Short-touch ecommerce item refresh (lucky bag drop refreshed). v3."""

    refreshToken: str
    protoVersion: int


class CapsuleEvent(TypedDict, total=False):
    """Capsule overlay (TikTok service-plus pin reminder). v3."""

    imageUrl: str
    titleKey: str
    btnKey: str
    deepLink: str
    reminderKey: str
    displayDurationSec: int
    protoVersion: int


class RoomVerifyEvent(TypedDict, total=False):
    """Room age / content classification verification event. v3."""

    verifyCode: int
    protoVersion: int


class SMBBoardEvent(TypedDict, total=False):
    """SMB (small-business) board overlay. v3."""

    boardPayload: str
    status: int
    protoVersion: int
