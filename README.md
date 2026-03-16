<p align="center">
  <img src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/banner.png" alt="tiktok-live-api Python" width="100%" />
</p>

# TikTok LIVE API — Python

### The managed TikTok Live connector for Python — receive chat, gifts, viewers, battles & 18+ events from any TikTok LIVE stream. Zero maintenance, zero breakages.

[![PyPI version](https://img.shields.io/pypi/v/tiktok-live-api?color=%23ff0050&logo=pypi&logoColor=white)](https://pypi.org/project/tiktok-live-api/)
[![PyPI downloads](https://img.shields.io/pypi/dm/tiktok-live-api)](https://pypi.org/project/tiktok-live-api/)
[![Python](https://img.shields.io/pypi/pyversions/tiktok-live-api)](https://pypi.org/project/tiktok-live-api/)
[![Stars](https://img.shields.io/github/stars/tiktool/tiktok-live-python?style=flat&color=0274b5)](https://github.com/tiktool/tiktok-live-python/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/1482387222912172159?logo=discord&label=Discord&color=5865F2)](https://discord.gg/y8TwuFBAmD)

<p align="center">
  <img src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/tiktok-live-api.gif" alt="TikTok Live API Demo — real-time chat, gifts, and viewer events" width="700">
</p>

> **99.9% uptime** — Never breaks when TikTok updates. No protobuf, no reverse engineering, no maintenance required. Powered by the [TikTool](https://tik.tools) managed WebSocket API.

<table>
<tr>
    <td><br/><img width="150px" src="https://raw.githubusercontent.com/tiktool/tiktok-live-python/main/.github/logo.png" alt="TikTool Logo"><br/><br/></td>
    <td>
        <a href="https://tik.tools">
            <strong>TikTool</strong> offers a fully managed TikTok LIVE API — real-time events, AI captions, CAPTCHA solving, and more. Free Sandbox tier. No credit card required.
        </a>
    </td>
</tr>
</table>

**🎤 Exclusive:** [Real-Time Live Captions](#-live-captions-speech-to-text) — AI-powered speech-to-text with translation & speaker diarization. **No other TikTok library offers this.**

## Table of Contents

- [Why tiktok-live-api?](#-why-tiktok-live-api)
- [Getting Started](#-getting-started)
- [Try It Now — 5-Minute Demo](#-try-it-now--5-minute-live-demo)
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
| **Maintenance** | ✅ Zero — we handle everything | ❌ You fix breakages | ❌ You fix breakages |
| **Multi-Language** | ✅ Python, Node.js, Java, Go, C# | Python only | Node.js only |
| **Free Tier** | ✅ 50 req/day, 5-min WS | ✅ Free (when it works) | ✅ Free (when it works) |

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

## 🚀 Try It Now — 5-Minute Live Demo

Copy-paste, run, see real-time TikTok events in your terminal. Works on the free Sandbox tier.

```python
# demo.py — TikTok LIVE in 5 minutes
# pip install tiktok-live-api
from tiktok_live_api import TikTokLive
import signal, sys

API_KEY       = "YOUR_API_KEY"        # Get free key → https://tik.tools
LIVE_USERNAME = "tv_asahi_news"       # Any live TikTok username

client = TikTokLive(LIVE_USERNAME, api_key=API_KEY)
events = 0

@client.on("connected")
def on_connected(event):
    print(f"\n✅ Connected to @{LIVE_USERNAME} — listening for 5 min...\n")

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
    print(f"\n📊 Done! Received {events} events.\n")

# Auto-exit after 5 minutes
if sys.platform != "win32":
    signal.alarm(300)

client.run()
```

<details>
<summary><strong>🔌 Pure WebSocket version (no SDK)</strong></summary>

```python
# ws-demo.py — Pure WebSocket, zero dependencies
# pip install websockets
import asyncio, websockets, json

API_KEY       = "YOUR_API_KEY"
LIVE_USERNAME = "tv_asahi_news"

async def listen():
    url = f"wss://api.tik.tools?uniqueId={LIVE_USERNAME}&apiKey={API_KEY}"
    events = 0
    async with websockets.connect(url) as ws:
        print(f"\n✅ Connected to @{LIVE_USERNAME} — listening for 5 min...\n")
        try:
            async for message in asyncio.wait_for(ws, timeout=300):
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
        except asyncio.TimeoutError:
            pass
    print(f"\n📊 Done! Received {events} events.\n")

asyncio.run(listen())
```

</details>

---

## 📋 Events

| Event | Description | Key Fields |
|-------|-------------|------------|
| `chat` | Chat message | `user`, `comment`, `emotes`, `starred?` |
| `gift` | Virtual gift | `user`, `giftName`, `diamondCount`, `repeatCount` |
| `like` | Like event | `user`, `likeCount`, `totalLikes` |
| `follow` | New follower | `user` |
| `share` | Stream share | `user` |
| `member` | Viewer joined | `user` |
| `subscribe` | New subscriber | `user` |
| `roomUserSeq` | Viewer count update | `viewerCount`, `topViewers` |
| `battle` | Battle event | `type`, `teams`, `scores` |
| `roomPin` | Pinned/starred message | `user`, `comment`, `action`, `durationSeconds` |
| `envelope` | Treasure chest | `diamonds`, `user` |
| `streamEnd` | Stream ended | `reason` |
| `connected` | WebSocket connected | `uniqueId` |
| `disconnected` | WebSocket disconnected | `uniqueId` |
| `error` | Error occurred | `error` |
| `event` | Catch-all (every event) | Full raw event payload |

All events include the full raw TikTok payload, giving you access to every field TikTok provides.

---

## 🎤 Live Captions (Speech-to-Text)

Transcribe and translate any TikTok LIVE stream in real-time. **This feature is unique to TikTool — no other TikTok library offers it.**

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
            print(f"  {i+1}. {name} — {diamonds} 💎")

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

## 💰 Pricing

| Tier | Requests/Day | WS Connections | WS Duration | Price |
|------|-------------|----------------|-------------|-------|
| **Sandbox** | 50 | 1 | 5 min | **Free** |
| **Basic** | 10,000 | 3 | 8 hours | $7/week |
| **Pro** | 75,000 | 50 | 8 hours | $15/week |
| **Ultra** | 300,000 | 500 | 8 hours | $45/week |

Get your free API key → [tik.tools](https://tik.tools)

---

## Star History

If this project helps you, please consider giving it a ⭐ — it helps others discover it!

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

- **TikTool** — *Creator & Maintainer* — [tik.tools](https://tik.tools)

See also the full list of [contributors](https://github.com/tiktool/tiktok-live-python/contributors) who have participated in this project.
