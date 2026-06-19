<p align="center">
  <a href="https://discord.com/oauth2/authorize?client_id=1482386543233597470">
    <img src="https://img.shields.io/badge/Add%20TikTool%20Bot%20to%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Add TikTool Bot to Discord" height="46">
  </a>
</p>

Agency rank feeds in Discord: gaming ranks, creator ranks and 99+ movers across all 30 regions, copy-paste usernames for backstage. /ranks to start (Global Agency).

<p align="center">
  <img src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/banner.png" alt="tiktok-live-api Python" width="100%" />
</p>

# TikTok LIVE API - Python

### The managed TikTok Live connector for Python - receive chat, gifts, viewers, battles & 18+ events from any TikTok LIVE stream. Zero maintenance, zero breakages.

[![PyPI version](https://img.shields.io/pypi/v/tiktok-live-api?color=%23ff0050&logo=pypi&logoColor=white)](https://pypi.org/project/tiktok-live-api/)
[![PyPI downloads](https://img.shields.io/pypi/dm/tiktok-live-api)](https://pypi.org/project/tiktok-live-api/)
[![Python](https://img.shields.io/pypi/pyversions/tiktok-live-api)](https://pypi.org/project/tiktok-live-api/)
[![Stars](https://img.shields.io/github/stars/tiktool/tiktok-live-python?style=flat&color=0274b5)](https://github.com/tiktool/tiktok-live-python/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/tiktok-live-api.gif" alt="TikTok Live API Demo - real-time chat, gifts, and viewer events" width="700">
</p>

> **99.9% uptime** - Never breaks when TikTok updates. No protobuf, no reverse engineering, no maintenance required. Powered by the [TikTool](https://tik.tools) managed WebSocket API.

<table>
<tr>
    <td><br/><img width="150px" src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/.github/logo.png" alt="TikTool Logo"><br/><br/></td>
    <td>
        <a href="https://tik.tools">
            <strong>TikTool</strong> offers a fully managed TikTok LIVE API - real-time events, AI captions, CAPTCHA solving, and more. Free Community tier (forever). No credit card required.
        </a>
    </td>
</tr>
</table>

**🎤 Exclusive:** [Real-Time Live Captions](#-live-captions-speech-to-text) - AI-powered speech-to-text with translation & speaker diarization. **No other TikTok library offers this.**

## 🚀 One-Command Quick Start

Instantly connect to a live TikTok stream and print real-time events to your terminal.

```bash
pip install tiktok-live-api
python -m tiktok_live_api
```
*Or connect to a specific stream:* `python -m tiktok_live_api @username`

---

## Table of Contents

- [Why tiktok-live-api?](#-why-tiktok-live-api)
- [Getting Started](#-getting-started)
- [Try It Now - Live Demo](#-try-it-now--live-demo)
- [Events](#-events)
- [Live Captions (AI STT)](#-live-captions-speech-to-text)
- [Async Usage](#-async-usage)
- [Chat Bot Example](#-chat-bot-example)
- [Other Languages](#-other-languages)
- [Pricing](#-pricing)
- [Star History](#star-history)
- [License](#license)

---

## 🆚 Why tiktok-live-api?

| | **tiktok-live-api** | TikTokLive (isaackogan) | TikTok-Live-Connector (Node.js) |
|---|---|---|---|
| **Stability** | ✅ Managed API, 99.9% uptime | ❌ Breaks on TikTok updates | ❌ Breaks on TikTok updates |
| **Setup** | ✅ 3 lines of code | ❌ Protobuf + reverse engineering | ❌ Protobuf + signing server |
| **Live Captions (AI STT)** | ✅ Real-time speech-to-text | ❌ Not available | ❌ Not available |
| **Translation** | ✅ 50+ languages | ❌ Not available | ❌ Not available |
| **CAPTCHA Solving** | ✅ Built-in (Pro+) | ❌ Manual | ❌ Manual |
| **Feed Discovery** | ✅ See who's live | ❌ Not available | ❌ Not available |
| **Maintenance** | ✅ Zero - we handle everything | ❌ You fix breakages | ❌ You fix breakages |
| **Multi-Language** | ✅ Python, Node.js, Java, Go, C# | Python only | Node.js only |
| **Free Tier** | ✅ 2,500 req/day, 15 WS, 2h per WS | ✅ Free (when it works) | ✅ Free (when it works) |

---

## ⚡ Getting Started

### 1. Install

```bash
pip install tiktok-live-api
```

### 2. Get your free API key

Go to [tik.tools](https://tik.tools) → Sign up → Copy your API key. No credit card required.

### 3. Connect

```python
from tiktok_live_api import TikTokLive

client = TikTokLive("streamer_username", api_key="YOUR_API_KEY")

@client.on("chat")
def on_chat(event):
    print(f"{event['user']['uniqueId']}: {event['comment']}")

@client.on("gift")
def on_gift(event):
    print(f"{event['user']['uniqueId']} sent {event['giftName']} ({event['diamondCount']} 💎)")

@client.on("roomUserSeq")
def on_viewers(event):
    print(f"Viewers: {event['viewerCount']}")

client.run()
```

That's it. **No protobuf, no signing servers, no reverse engineering, no breakages.**

---

## 🚀 Try It Now - Live Demo

Copy-paste, run, see real-time TikTok events in your terminal. Works on the free **Community** tier - 2h per WS, runs as long as the stream is live.

```python
# demo.py - TikTok LIVE in real time
# pip install tiktok-live-api
from tiktok_live_api import TikTokLive

API_KEY       = "YOUR_API_KEY"        # Get free key → https://tik.tools
LIVE_USERNAME = "tv_asahi_news"       # Any live TikTok username

client = TikTokLive(LIVE_USERNAME, api_key=API_KEY)
events = 0

@client.on("connected")
def on_connected(event):
    print(f"\n✅ Connected to @{LIVE_USERNAME} - streaming events...\n")

@client.on("chat")
def on_chat(event):
    global events; events += 1
    print(f"💬 {event['user']['uniqueId']}: {event['comment']}")

@client.on("gift")
def on_gift(event):
    global events; events += 1
    print(f"🎁 {event['user']['uniqueId']} sent {event['giftName']} ({event.get('diamondCount', 0)}💎)")

@client.on("like")
def on_like(event):
    global events; events += 1
    print(f"❤️  {event['user']['uniqueId']} liked × {event.get('likeCount', 0)}")

@client.on("member")
def on_member(event):
    global events; events += 1
    print(f"👋 {event['user']['uniqueId']} joined")

@client.on("roomUserSeq")
def on_viewers(event):
    global events; events += 1
    print(f"👀 Viewers: {event['viewerCount']}")

@client.on("disconnected")
def on_disconnect(event):
    print(f"\n📊 Disconnected. Received {events} events.\n")

# Press Ctrl+C to stop. Community tier caps each WebSocket at 2 hours.
client.run()
```

<details>
<summary><strong>🔌 Pure WebSocket version (no SDK)</strong></summary>

```python
# ws-demo.py - Pure WebSocket, zero dependencies
# pip install websockets
import asyncio, websockets, json

API_KEY       = "YOUR_API_KEY"
LIVE_USERNAME = "tv_asahi_news"

async def listen():
    url = f"wss://api.tik.tools?uniqueId={LIVE_USERNAME}&apiKey={API_KEY}"
    events = 0
    async with websockets.connect(url) as ws:
        print(f"\n✅ Connected to @{LIVE_USERNAME} - streaming events...\n")
        async for message in ws:
            msg = json.loads(message)
            events += 1
            data = msg.get("data", {})
            user = data.get("user", {}).get("uniqueId", "")
            event = msg.get("event", "")
            if event == "chat":        print(f"💬 {user}: {data.get('comment', '')}")
            elif event == "gift":      print(f"🎁 {user} sent {data.get('giftName', '')}")
            elif event == "like":      print(f"❤️  {user} liked × {data.get('likeCount', 0)}")
            elif event == "member":    print(f"👋 {user} joined")
            elif event == "roomUserSeq": print(f"👀 Viewers: {data.get('viewerCount', 0)}")
            else:                      print(f"📦 {event}")
    print(f"\n📊 Disconnected. Received {events} events.\n")

asyncio.run(listen())
```

</details>

---

## 📋 Events (54 v3 event types)

Every event is dispatched by name. Each event payload extends the `BaseEvent` shape (`type`, `timestamp`, `msgId`, optional `protoVersion: 1 | 2 | 3`).

### Core live events

| Event | Description |
|---|---|
| `connected` | WebSocket open. |
| `disconnected` | WebSocket close. |
| `roomInfo` | One-shot post-connect: `{ roomId, wsHost, clusterRegion, connectedAt }`. |
| `chat` | Chat message. `user`, `comment`, `emotes`, optional `starred`. **v3** adds `language` (auto-detected ISO 639-1) + `messageUuid` (moderation correlation). |
| `gift` | Virtual gift. `giftId`, `giftName`, `diamondCount`, `repeatCount`, `repeatEnd`, `giftType`. **v3** adds `transactionId` (dedup key), `senderUserId`, `relationship` (`joinDayNumber`, `fromUser`, `toUser`). |
| `like` | Like batch. `likeCount`, `totalLikes`. |
| `member` | Viewer joined. **v3** adds `actionCode`, `entrySource` (`"homepage_hot-live_cell"`, `"follow-tab"`, ...), `entryAction` (`"draw"`/`"click"`), `entryType` (`"rec"` = algorithmic). |
| `social` | Follow / share. |
| `roomUserSeq` | Periodic viewer count tick. |
| `subscribe` | A viewer subscribed. |

### PK / battle events

| Event | Description |
|---|---|
| `battle` | PK lifecycle. `status` (1=ACTIVE, 2=STARTING, 3=ENDED, 4=PREPARING), `battleDuration`, `teams`. **v3** adds `extraHostUserIds`, `layoutSubtype`. |
| `battleArmies` | Per-host MVP breakdown. `hosts[].contributors[]` sorted MVP first. **v3** adds `transactionId`. |
| `battleItemCard` | Booster card: x2/x3 multipliers, gloves (crit), mist, thunder, extra-time, match-guide. Carries TikTok CDN overlay assets. |
| `battlePunishFinish` | Loser-side punishment screen ended. |
| `battleNotice` | PK notice (version-mismatch toast, invite-failure). |
| `battleGameplay` | PK mini-game state. |
| `linkLayer` | PK / link-mic negotiation. |
| `linkMicOpponentGift` | Per-gift breakdown from the OPPONENT side of a PK. |
| `linkScreenChange` | PK split-screen layout flip. |
| `cohostLayoutUpdate` | Cohost layout subtype change. |
| `linkMic`, `linkMicLayoutState`, `link` | Generic link-mic envelopes. |
| `competition`, `competitionContributor` | Cross-stream competition + per-contributor breakdown. |
| `guestShowdown` | Guest showdown lifecycle. |

### Native captions (v3)

| Event | Description |
|---|---|
| `caption` | **NEW in v3.** TikTok native auto-captions on the LIVE WebSocket. `text`, `isFinal`, `startedAtMs`, `endsAtMs`. Independent of the operator-managed [TikTok Live Captions](https://tik.tools/captions) product. |

### Creator-side events

| Event | Description |
|---|---|
| `goalUpdate` | Stream goal progress (subscriber / gift / watch-time goals). |
| `commentTray` | Comment tray UI state change. |
| `roomPin` | A chat got pinned by the host or a moderator. |
| `hostBoard` | Host leaderboard board update. |
| `privilegeAdvance` | Viewer privilege tier-up notification. |
| `anchorToolModification` | Creator modified a panel/widget. |
| `inRoomBanner` | In-room activity banner. |
| `roomSticker` | Room-wide sticker drop. |
| `bottomMessage` | Bottom-bar safety / risk notice. |
| `accessRecall`, `roomVerify` | Content-classification recheck events. |
| `smbBoard` | SMB (small-business) board overlay. |
| `streamStatus` | Stream status flip. |
| `shareRevenueNotice` | Share-revenue subscriber count change. |
| `capsule` | TikTok service-plus pin reminder. |
| `hotRoom` | TikTok promoted the room to a high-traffic slot. |
| `linkMicAnchorGuide` | Anchor (creator) guide nudges. |

### Moderation / safety

| Event | Description |
|---|---|
| `imDelete` | Chat moderation delete. Correlate via `chat.messageUuid` (v3). |
| `unauthorizedMember` | Unauthorized viewer hit a gated feature. |
| `barrage` | Raw barrage feed. |
| `superFan`, `superFanJoin`, `superFanBox` | Super-fan lifecycle. |
| `emoteChat` | Inline emote message. |

### Gift catalog + ecommerce

| Event | Description |
|---|---|
| `giftPanelUpdate` | Real-time gift catalog change. Cache-bust your local catalog. |
| `giftDynamicRestriction` | Per-room gift availability flip / age-gating. |
| `giftGallery` | Host-side gift wall snapshot. |
| `giftUnlock` | Host unlocked a gated gift. |
| `viewerPicksUpdate` | TikTok-promoted viewer-pick gift highlights. |
| `oecLiveShopping`, `oecLiveManager`, `oecLiveBillboard` | OEC live-shopping events. |
| `ecShortItemRefresh` | Lucky-bag drop refreshed. |

### Engagement + AI

| Event | Description |
|---|---|
| `aiSummary` | TikTok AI summary of the room (entry-time recap, multi-language). |
| `poll`, `shortTouch` | In-stream poll lifecycle. |
| `rankText`, `rankUpdate`, `hourlyRank` | Rank events. |
| `question`, `questionSelected`, `questionSlideDown` | Q&A round events. |
| `pictionaryUpdate`, `pictionaryEnd`, `pictionaryExit` | Drawing-game round events. |
| `fansEvent`, `fanTicket` | Fan-club events. |
| `envelope`, `envelopePortal` | Red-envelope drops + multi-room portal chain. |
| `gameMoment`, `gameServerFeature` | TikTok Gaming live integration. |
| `groupLiveMemberNotify` | Group-live member join / leave. |
| `perception` | Perception event (mute cancel, TikTok hint signal). |
| `control`, `room`, `liveIntro` | Stream control + room metadata. |

### Catch-all

- `event` - Fires for every decoded event.
- `unknown` - Fires when TikTok ships a method we don't yet model (forward-compat hook).

All events ship with full TypedDict annotations. Your IDE shows autocompletion for every field. See [full per-event JSON examples + field tables](https://tik.tools/docs).

### Battle / PK example

```python
from tiktok_live_api import TikTokLive

client = TikTokLive(unique_id="creator_username", api_key="tk_...")

@client.on("battle")
def on_battle(e):
    print(f"PK status={e['status']} id={e['battleId']} duration={e['battleDuration']}s")

@client.on("battleArmies")
def on_armies(e):
    print(f"Countdown: {e.get('secsRemaining')}s")
    for host in e.get("hosts", []):
        print(f"  @{host['hostUserId']} total={host['teamTotalScore']}")
        if host["contributors"]:
            mvp = host["contributors"][0]
            print(f"    MVP {mvp['nickname']} score={mvp['score']}")

@client.on("battleItemCard")
def on_card(e):
    if e["multiplier"] > 0:
        print(f"x{e['multiplier']} booster from @{e['senderUniqueId']}")
    else:
        print(f"Effect {e['effect']} from @{e['senderUniqueId']} ({e['durationSec']}s)")

client.connect()
```


---

## 🎤 Live Captions (Speech-to-Text)

Transcribe and translate any TikTok LIVE stream in real-time. **This feature is unique to TikTool - no other TikTok library offers it.**

```python
from tiktok_live_api import TikTokCaptions

captions = TikTokCaptions(
    "streamer_username",
    api_key="YOUR_API_KEY",
    translate="en",       # translate to English (50+ languages)
    diarization=True,     # identify who is speaking
)

@captions.on("caption")
def on_caption(event):
    speaker = event.get("speaker", "")
    text = event["text"]
    is_final = event.get("isFinal", False)
    print(f"[{speaker}] {text}{'  ✓' if is_final else '...'}")

@captions.on("translation")
def on_translation(event):
    print(f"  → {event['text']}")

captions.run()
```

### Caption Events

| Event | Description | Key Fields |
|-------|-------------|------------|
| `caption` | Real-time caption text | `text`, `speaker`, `isFinal`, `language` |
| `translation` | Translated caption | `text`, `sourceLanguage`, `targetLanguage` |
| `credits` | Credit balance update | `total`, `used`, `remaining` |

---

## 🔄 Async Usage

For integration with async frameworks (FastAPI, Django Channels, etc.):

```python
import asyncio
from tiktok_live_api import TikTokLive

async def main():
    client = TikTokLive("streamer_username", api_key="YOUR_API_KEY")

    @client.on("chat")
    async def on_chat(event):
        print(f"{event['user']['uniqueId']}: {event['comment']}")

    await client.connect()

asyncio.run(main())
```

---

## 🤖 Chat Bot Example

```python
from tiktok_live_api import TikTokLive

client = TikTokLive("streamer_username", api_key="YOUR_API_KEY")
gift_leaderboard = {}
message_count = 0

@client.on("chat")
def on_chat(event):
    global message_count
    message_count += 1
    msg = event["comment"].lower().strip()
    user = event["user"]["uniqueId"]

    if msg == "!hello":
        print(f">> BOT: Welcome {user}! 👋")
    elif msg == "!stats":
        print(f">> BOT: {message_count} messages, {len(gift_leaderboard)} gifters")
    elif msg == "!top":
        top = sorted(gift_leaderboard.items(), key=lambda x: -x[1])[:5]
        for i, (name, diamonds) in enumerate(top):
            print(f"  {i+1}. {name} - {diamonds} 💎")

@client.on("gift")
def on_gift(event):
    user = event["user"]["uniqueId"]
    diamonds = event.get("diamondCount", 0)
    gift_leaderboard[user] = gift_leaderboard.get(user, 0) + diamonds

client.run()
```

---

## 🌐 Other Languages

TikTool Live is available in every major language:

| Language | Package | Install |
|----------|---------|---------|
| **Python** | [tiktok-live-api](https://pypi.org/project/tiktok-live-api/) | `pip install tiktok-live-api` |
| **Node.js / TypeScript** | [@tiktool/live](https://www.npmjs.com/package/@tiktool/live) | `npm install @tiktool/live` |
| **Any Language** | [WebSocket API](https://tik.tools/docs) | `wss://api.tik.tools?uniqueId=USERNAME&apiKey=KEY` |

Full documentation with examples in **Java, Go, C#, cURL** → [tik.tools/docs](https://tik.tools/docs)

---

## Environment Variable

Instead of passing `api_key` directly, set it as an environment variable:

```bash
# Linux / macOS
export TIKTOOL_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:TIKTOOL_API_KEY="your_api_key_here"
```

```python
from tiktok_live_api import TikTokLive

# Automatically reads TIKTOOL_API_KEY from environment
client = TikTokLive("streamer_username")
client.on("chat", lambda e: print(e["comment"]))
client.run()
```

---

## Pricing (USD)
| Tier | Weekly | Monthly |
|------|--------|---------|
| Sandbox / Free | $0 | $0 |
| Basic | $7 | $19 |
| Pro | $15 | $49 |
| Ultra | $45 | $149 |
| Global Agency | $119 | $399 |

Full pricing + checkout: https://tik.tools/pricing

## Tiers
Tier ladder (each includes everything below it): Sandbox -> Basic -> Pro -> Ultra -> Global Agency. Sandbox is free with reduced rate limits + masked identifiers on intelligence endpoints; paid tiers raise limits and unmask data. Outgoing webhooks need Basic+. The agency intelligence endpoints (gaming ranks, movers, eligible-creator finder, gifter intel) need Global Agency.

## Endpoints and required tier
| Endpoint | Min tier |
|---|---|
| POST /webcast/sign_url | Sandbox |
| POST /webcast/sign_websocket | Sandbox |
| GET /webcast/ws_credentials | Sandbox |
| GET /webcast/fetch | Sandbox |
| GET /webcast/room_id | Sandbox |
| GET /webcast/room_info | Sandbox |
| GET /webcast/room_video | Sandbox |
| GET /webcast/room_cover | Sandbox |
| GET /webcast/check_alive | Sandbox |
| POST /webcast/bulk_live_check | Sandbox |
| GET /webcast/live_status | Sandbox |
| GET /webcast/live-counts | Sandbox |
| POST /webcast/resolve_user_ids | Sandbox |
| GET /webcast/rankings | Sandbox |
| GET /webcast/leaderboard | Sandbox |
| GET /webcast/leaderboard/league | Sandbox |
| GET /webcast/leaderboard/leagues | Sandbox |
| GET /webcast/gift_info | Sandbox |
| GET /webcast/gift_gallery | Sandbox |
| GET /webcast/hashtag_list | Sandbox |
| GET /webcast/user_earnings | Sandbox |
| GET /webcast/live_analytics/video_list | Sandbox |
| GET /webcast/live_analytics/video_detail | Sandbox |
| GET /webcast/live_analytics/user_interactions | Sandbox |
| GET /webcast/rate_limits | Sandbox |
| POST /authentication/jwt | Sandbox |
| GET /api/live/connect | Sandbox |
| POST /chat-send | Basic |
| GET/POST /api/webhooks | Basic |
| POST /api/webhooks/{id}/test | Basic |
| GET /ws/sweep | Basic |
| GET /webcast/feed | Pro |
| POST /webcast/ranklist/regional | Pro |
| GET /webcast/user_profile | Pro |
| GET /api/leaderboards/country/:slug | Pro |
| GET /webcast/gifts_by_country | Ultra |
| GET /api/leaderboards/leagues/:region | Ultra |
| GET /api/leaderboards/league/:region/:classType | Ultra |
| GET /webcast/ranklist/gaming | Global Agency |
| GET /webcast/ranklist/gaming_movers | Global Agency |
| GET /webcast/ranklist/region_movers | Global Agency |
| GET /webcast/eligible_creators | Global Agency |
| GET /api/gifters/top | Global Agency |
| GET /api/gifters/leaderboard | Global Agency |
| GET /api/gifters/profile | Global Agency |

Full docs with request/response shapes and examples: https://tik.tools/docs

## What you get
**Creators**: real-time live events (gifts, chat, viewers), your own live status + room info, earnings + analytics, signed CDN/stream URLs that do not expire.
**Developers**: drop-in signing (works as a tiktok-live-connector backend - point the sign base at api.tik.tools), one-WebSocket fan-out (your IP never touches TikTok), bulk live checks, leaderboards, webhooks (HMAC-signed live.start/live.end and more), SDKs across languages.
**Agencies (Global Agency)**: TikTok LIVE gaming ranks + creator ranks + 99+ movers across all 30 regions, eligible-creator recruiting finder, gifter intelligence (top gifters, profiles, leaderboards), and the Discord bot that posts copy-paste username batches for backstage.

### Live Gifter Firehose - Global Agency

Real-time gift event stream. Filter by region, league, or globally; cap by minimum diamond threshold.

```python
import asyncio, json, websockets

API_KEY = "tk_..."
URL = f"wss://api.tik.tools/firehose/gifters?apiKey={API_KEY}&mode=region&region=US%2B&min_diamonds=1000"

async def main():
    async with websockets.connect(URL) as ws:
        async for raw in ws:
            evt = json.loads(raw)
            # evt: { type:'gifter_alert', ts, gifter:{username,displayName,isAnonymous},
            #        creator:{uniqueId}, gift:{name,totalDiamonds}, region }
            print(evt)

asyncio.run(main())
```

Modes: `global` (all regions), `region` (single region code), `league` (region + league class, e.g. `B2`). Update the filter mid-stream by sending `{"type":"update_filter","mode":"global","min_diamonds":5000}` - no reconnect needed.

Get your free API key → [tik.tools](https://tik.tools)

---

## Star History

If this project helps you, please consider giving it a ⭐ - it helps others discover it!

<p align="center">
    <a href="https://github.com/tiktool/tiktok-live-python/stargazers">
        <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=tiktool/tiktok-live-python&type=Date&theme=dark" onerror="this.src='https://api.star-history.com/svg?repos=tiktool/tiktok-live-python&type=Date'" />
    </a>
</p>

---

## Links

- 🌐 **Website**: [tik.tools](https://tik.tools)
- 📖 **Documentation**: [tik.tools/docs](https://tik.tools/docs)
- 📦 **Node.js SDK**: [@tiktool/live on npm](https://www.npmjs.com/package/@tiktool/live)
- 🐍 **PyPI**: [tiktok-live-api](https://pypi.org/project/tiktok-live-api/)
- 💻 **GitHub (Node.js)**: [tiktool/tiktok-live-api](https://github.com/tiktool/tiktok-live-api)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

- **TikTool** - *Creator & Maintainer* - [tik.tools](https://tik.tools)

See also the full list of [contributors](https://github.com/tiktool/tiktok-live-python/contributors) who have participated in this project.
