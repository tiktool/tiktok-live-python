import sys
import asyncio
import json
import time
try:
    import websockets
except ImportError:
    print("tiktok-live-api python CLI requires websockets.")
    print("Please install via: pip install tiktok-live-api")
    sys.exit(1)

WS_BASE = "wss://api.tik.tools"
DEMO_KEY = "demo_tiktokliveapi_public_2026"

CHANNELS = [
    'aljazeeraenglish', 'cgtnofficial', 'france24_en',
    'weathernewslive', 'gbnews', 'bbcnews',
    'skynews', 'tv_asahi_news', 'abc7chicago', 'thairath_news',
]

# ── ANSI ───────────────────────────────────────────────────────────────
R  = '\x1b[0m'
B  = '\x1b[1m'
D  = '\x1b[2m'
C_CYAN = '\x1b[38;5;80m'
C_GREEN = '\x1b[38;5;114m'
C_YELLOW = '\x1b[38;5;222m'
C_MAG = '\x1b[38;5;176m'
C_BLUE = '\x1b[38;5;111m'
C_RED = '\x1b[38;5;203m'
C_GRAY = '\x1b[38;5;242m'
C_WHITE = '\x1b[38;5;252m'

TAG = {
    'chat': f"{C_CYAN}chat{R}",
    'gift': f"{C_YELLOW}gift{R}",
    'like': f"{C_MAG}like{R}",
    'member': f"{C_GREEN}join{R}",
    'follow': f"{C_GREEN}follow{R}",
    'viewer': f"{C_BLUE}viewers{R}",
    'share': f"{C_WHITE}share{R}",
    'roomUserSeq': f"{C_BLUE}viewers{R}",
}

def help_msg():
    print(f"""
  {B}tiktok-live-api{R}  {D}Real-time TikTok Live events in your terminal{R}

  {B}Usage{R}
    {C_CYAN}python -m tiktok_live_api{R}                  {D}auto-find a live stream{R}
    {C_CYAN}python -m tiktok_live_api{R} {C_WHITE}@username{R}        {D}connect to a specific user{R}
    {C_CYAN}python -m tiktok_live_api{R} {C_GRAY}--key KEY{R}        {D}use your own API key{R}

  {D}Unofficial third-party API by TikTool{R}
  {D}https://tik.tools · Not affiliated with TikTok or ByteDance{R}
""")

async def probe(uid, api_key, timeout_ms=8000):
    url = f"{WS_BASE}?uniqueId={uid}&apiKey={api_key}"
    try:
        ws = await asyncio.wait_for(websockets.connect(url), timeout=timeout_ms / 1000.0)
        return ws
    except Exception:
        return None

def banner():
    print()
    print(f"  {B}tiktok-live-api{R}  {D}·{R}  {D}Real-time TikTok Live events{R}")
    print(f"  {D}Unofficial API by TikTool · https://tik.tools{R}")
    print()

def ts():
    import datetime
    return f"{C_GRAY}{datetime.datetime.now().strftime('%H:%M:%S')}{R}"

def fmt(event, data):
    # Some events like roomUserSeq should map to 'viewer' visually
    vis_event = 'viewer' if event == 'roomUserSeq' else event
    tag = TAG.get(vis_event, f"{C_GRAY}{event.ljust(7)}{R}")
    pad = "  " if vis_event in TAG else " "
    
    u = data.get('user', {}).get('uniqueId', '')

    if event == 'chat':
        return f"{ts()} {tag}{pad}  {B}{u}{R}  {data.get('comment', '')}"
    elif event == 'gift':
        name = data.get('giftName', 'gift')
        n = data.get('repeatCount', 1)
        d2 = data.get('diamondCount', 0)
        return f"{ts()} {tag}{pad}  {B}{u}{R}  {C_YELLOW}{name}{R} x{n} {D}({d2}💎){R}"
    elif event == 'like':
        return f"{ts()} {tag}{pad}  {B}{u}{R}  {D}total {data.get('totalLikeCount', 0):,}{R}"
    elif event == 'member':
        return f"{ts()} {tag}{pad}  {C_GREEN}{u}{R}"
    elif event == 'follow':
        return f"{ts()} {tag}  {C_GREEN}{u}{R}"
    elif event == 'roomUserSeq':
        return f"{ts()} {tag}  {B}{data.get('viewerCount', 0):,}{R}"
    elif event == 'share':
        return f"{ts()} {tag} {u}"
    return None

async def async_main():
    api_key = DEMO_KEY
    target = ""
    args = sys.argv[1:]
    
    i = 0
    while i < len(args):
        a = args[i]
        if a in ('--key', '-k'):
            i += 1
            if i < len(args): api_key = args[i]
        elif a in ('--help', '-h'):
            help_msg()
            sys.exit(0)
        elif not a.startswith('-'):
            target = a.lstrip('@')
        i += 1

    banner()
    ws = None
    who = ""

    if target:
        sys.stdout.write(f"  {D}connecting to{R} {B}@{target}{R} {D}...{R}")
        sys.stdout.flush()
        ws = await probe(target, api_key)
        if ws:
            who = target
            print(f" {C_GREEN}●{R}")
        else:
            print(f" {C_RED}✗{R}\n\n  {C_RED}Stream not found.{R} Make sure {B}@{target}{R} is live.\n")
            sys.exit(1)
    else:
        print(f"  {D}scanning for live streams...{R}\n")
        for uid in CHANNELS:
            sys.stdout.write(f"  {C_GRAY}@{uid}{R}")
            sys.stdout.flush()
            ws = await probe(uid, api_key)
            if ws:
                who = uid
                print(f"  {C_GREEN}● live{R}")
                break
            else:
                print(f"  {D}-{R}")
        
        if not ws:
            print(f"\n  {C_RED}No live streams found.{R} Try: {C_CYAN}python -m tiktok_live_api @username{R}\n")
            print(f"  {D}Get your own API key at{R} {C_CYAN}https://tik.tools{R}\n")
            sys.exit(1)

    print()
    print(f"  {C_GREEN}●{R} {B}@{who}{R}  {D}- streaming events. Ctrl+C to stop.{R}")
    print(f"  {D}{'─' * 50}{R}")
    print()

    count = 0
    try:
        async for message in ws:
            try:
                m = json.loads(message)
                ev = m.get('event', 'unknown')
                d = m.get('data', m)
                line = fmt(ev, d)
                if line:
                    count += 1
                    print(f"  {line}")
            except Exception:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    except asyncio.CancelledError:
        pass
    finally:
        print(f"\n\n  {D}stopped - {B}{count}{R}{D} events received{R}")
        print(f"  {D}Get unlimited access:{R} {C_CYAN}https://tik.tools{R}\n")
        if ws: await ws.close()

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass # Handle Ctrl+C silently as the finally block prints the end message

if __name__ == '__main__':
    main()
