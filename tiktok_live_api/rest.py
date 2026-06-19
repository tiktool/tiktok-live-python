"""TikTool REST client - async methods for every customer-facing tik.tools
REST endpoint. Pairs with the TikTokLive WebSocket client.

Example:
    from tiktok_live_api import TikTool

    api = TikTool(api_key="YOUR_KEY")
    status = await api.live_status("charlidamelio")
    board = await api.leaderboard(region="US+")
    recruits = await api.eligible_creators(region="US+", limit=50)

Uses stdlib urllib in a worker thread, so it adds no dependencies and never
blocks the event loop.
"""

import asyncio
import json
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Optional

REST_BASE = "https://api.tik.tools"


class TikToolError(Exception):
    """Raised when an endpoint returns a non-2xx status. ``body`` holds the parsed payload."""

    def __init__(self, status: int, body: Any) -> None:
        self.status = status
        self.body = body
        msg = body.get("error") if isinstance(body, dict) and "error" in body else f"Request failed with status {status}"
        super().__init__(str(msg))


class TikTool:
    def __init__(self, api_key: str, base_url: str = REST_BASE) -> None:
        if not api_key:
            raise ValueError("TikTool requires an api_key")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    def _uid(self, unique_id: str) -> dict:
        # The API is inconsistent about unique_id / username / uniqueId; send all.
        return {"unique_id": unique_id, "username": unique_id, "uniqueId": unique_id}

    def _do(self, path: str, method: str, query: Optional[dict], body: Optional[dict]) -> Any:
        url = self._base_url + path
        if query:
            clean = {k: v for k, v in query.items() if v is not None}
            if clean:
                url += "?" + urllib.parse.urlencode(clean)
        data = json.dumps(body).encode() if body is not None else None
        headers = {"x-api-key": self._api_key}
        if data is not None:
            headers["content-type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode()
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                parsed = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                parsed = raw
            raise TikToolError(e.code, parsed) from None
        try:
            return json.loads(raw) if raw else None
        except json.JSONDecodeError:
            return raw

    async def request(self, path: str, method: str = "GET", query: Optional[dict] = None, body: Optional[dict] = None) -> Any:
        """Low-level request. Use the named methods below; exposed for unwrapped endpoints."""
        return await asyncio.to_thread(self._do, path, method, query, body)

    # --- Signing / connection ---
    async def sign_url(self, url: str): return await self.request("/webcast/sign_url", "POST", body={"url": url})
    async def sign_websocket(self, body: dict): return await self.request("/webcast/sign_websocket", "POST", body=body)
    async def ws_credentials(self, unique_id: str): return await self.request("/webcast/ws_credentials", query=self._uid(unique_id))
    async def connection_mode(self, unique_id: str): return await self.request("/webcast/connection_mode", query=self._uid(unique_id))
    async def check_alive(self, unique_id: str): return await self.request("/webcast/check_alive", query=self._uid(unique_id))
    async def rate_limits(self): return await self.request("/webcast/rate_limits")
    async def ws_sessions(self): return await self.request("/webcast/ws_sessions")
    async def jwt(self, body: Optional[dict] = None): return await self.request("/authentication/jwt", "POST", body=body or {})

    # --- Live status ---
    async def is_live(self, unique_id: str): return await self.request("/webcast/is_live", query=self._uid(unique_id))
    async def live_status(self, unique_id: str): return await self.request("/webcast/live_status", query=self._uid(unique_id))
    async def bulk_live_check(self, usernames: list): return await self.request("/webcast/bulk_live_check", "POST", body={"usernames": usernames})
    async def live_counts(self, region: Optional[str] = None): return await self.request("/webcast/live_counts", query={"region": region})
    async def room_id(self, unique_id: str): return await self.request("/webcast/room_id", query=self._uid(unique_id))
    async def room_info(self, unique_id: str): return await self.request("/webcast/room_info", query=self._uid(unique_id))
    async def room_cover(self, unique_id: str): return await self.request("/webcast/room_cover", query=self._uid(unique_id))
    async def room_video(self, unique_id: str): return await self.request("/webcast/room_video", query=self._uid(unique_id))

    # --- Rankings / leaderboards ---
    async def rankings(self, **query): return await self.request("/webcast/rankings", query=query)
    async def ranklist(self, **query): return await self.request("/webcast/ranklist", query=query)
    async def ranklist_regional(self, region: str): return await self.request("/webcast/ranklist/regional", query={"region": region})
    async def ranklist_gaming(self, region: str): return await self.request("/webcast/ranklist/gaming", query={"region": region})
    async def gaming_movers(self, region: str): return await self.request("/webcast/ranklist/gaming_movers", query={"region": region})
    async def region_movers(self, region: str): return await self.request("/webcast/ranklist/region_movers", query={"region": region})
    async def leaderboard(self, region: str, **query): return await self.request("/webcast/leaderboard", query={"region": region, **query})
    async def eligible_creators(self, **query): return await self.request("/webcast/eligible_creators", query=query)

    # --- Gifts ---
    async def gift_info(self, **query): return await self.request("/webcast/gift_info", query=query)
    async def gift_gallery(self, **query): return await self.request("/webcast/gift_gallery", query=query)
    async def gifts_by_country(self, country: str): return await self.request("/webcast/gifts_by_country", query={"country": country})

    # --- User / profile ---
    async def lookup_username(self, unique_id: str): return await self.request("/webcast/lookup_username", query=self._uid(unique_id))
    async def profile_info(self, unique_id: str): return await self.request("/webcast/profile_info", query=self._uid(unique_id))
    async def resolve_user_ids(self, usernames: list): return await self.request("/webcast/resolve_user_ids", "POST", body={"usernames": usernames})
    async def user_profile(self, unique_id: str): return await self.request("/webcast/user_profile", query=self._uid(unique_id))
    async def user_videos(self, unique_id: str, **query): return await self.request("/webcast/user_videos", query={**self._uid(unique_id), **query})
    async def user_followers(self, unique_id: str, **query): return await self.request("/webcast/user_followers", query={**self._uid(unique_id), **query})
    async def user_following(self, unique_id: str, **query): return await self.request("/webcast/user_following", query={**self._uid(unique_id), **query})
    async def user_likes(self, unique_id: str, **query): return await self.request("/webcast/user_likes", query={**self._uid(unique_id), **query})
    async def user_earnings(self, unique_id: str): return await self.request("/webcast/user_earnings", query=self._uid(unique_id))

    # --- Content / feed ---
    async def hashtag_list(self, **query): return await self.request("/webcast/hashtag_list", query=query)
    async def fetch(self, body: dict): return await self.request("/webcast/fetch", "POST", body=body)
    async def feed(self, **query): return await self.request("/webcast/feed", query=query)
    async def chat(self, unique_id: str, **query): return await self.request("/webcast/chat", query={**self._uid(unique_id), **query})

    # --- Live analytics ---
    async def analytics_video_list(self, **query): return await self.request("/webcast/live_analytics/video_list", query=query)
    async def analytics_video_detail(self, **query): return await self.request("/webcast/live_analytics/video_detail", query=query)
    async def analytics_user_interactions(self, **query): return await self.request("/webcast/live_analytics/user_interactions", query=query)

    # --- Moderation ---
    async def moderation_mutes(self, unique_id: str): return await self.request("/webcast/moderation/mutes", query=self._uid(unique_id))
    async def moderation_bans(self, unique_id: str): return await self.request("/webcast/moderation/bans", query=self._uid(unique_id))

    # --- CAPTCHA solver (Pro+) ---
    async def solve_puzzle(self, body: dict): return await self.request("/captcha/solve/puzzle", "POST", body=body)
    async def solve_rotate(self, body: dict): return await self.request("/captcha/solve/rotate", "POST", body=body)
    async def solve_shapes(self, body: dict): return await self.request("/captcha/solve/shapes", "POST", body=body)

    # --- Captions ---
    async def captions_credits(self): return await self.request("/captions/credits")
