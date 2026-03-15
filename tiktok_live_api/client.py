"""TikTokLive client — connect to any TikTok LIVE stream via WebSocket."""
# ruff: noqa: E402

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
from typing import Any, Callable, Dict, List, Optional, Union

import websockets
import websockets.client

logger = logging.getLogger("tiktok_live_api")

EventHandler = Callable[[Dict[str, Any]], None]
AsyncEventHandler = Callable[[Dict[str, Any]], Any]
AnyHandler = Union[EventHandler, AsyncEventHandler]

WS_BASE = "wss://api.tik.tools"
_VERSION = "1.0.1"


class TikTokLive:
    """Connect to a TikTok LIVE stream and receive real-time events.

    Args:
        unique_id: TikTok username (without @).
        api_key: Your TikTool API key. Get one free at https://tik.tools
        auto_reconnect: Auto-reconnect on disconnect (default True).
        max_reconnect_attempts: Max reconnection attempts (default 5).

    Example::

        from tiktok_live_api import TikTokLive

        client = TikTokLive("streamer_username", api_key="YOUR_KEY")

        @client.on("chat")
        def on_chat(event):
            print(f"{event['user']['uniqueId']}: {event['comment']}")

        client.run()
    """

    def __init__(
        self,
        unique_id: str,
        *,
        api_key: Optional[str] = None,
        auto_reconnect: bool = True,
        max_reconnect_attempts: int = 5,
    ) -> None:
        self.unique_id = unique_id.lstrip("@")
        self.api_key = api_key or os.environ.get("TIKTOOL_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "api_key is required. Get a free key at https://tik.tools"
            )
        self.auto_reconnect = auto_reconnect
        self.max_reconnect_attempts = max_reconnect_attempts

        self._handlers: Dict[str, List[AnyHandler]] = {}
        self._ws: Optional[websockets.client.WebSocketClientProtocol] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connected = False
        self._intentional_close = False
        self._reconnect_attempts = 0
        self._event_count = 0

    @property
    def connected(self) -> bool:
        """Whether the client is currently connected."""
        return self._connected

    @property
    def event_count(self) -> int:
        """Total number of events received."""
        return self._event_count

    def on(
        self, event: str, handler: Optional[AnyHandler] = None
    ) -> Any:
        """Register an event handler. Can be used as a decorator or called directly.

        Supported events:
            connected, chat, gift, like, follow, share, member, subscribe,
            roomUserSeq, roomPin, roomInfo, battle, envelope, streamEnd,
            error, disconnected, event (catch-all)

        Usage as decorator::

            @client.on("chat")
            def on_chat(event):
                print(event["comment"])

        Usage as method::

            client.on("gift", lambda e: print(e["giftName"]))
        """
        if handler is not None:
            self._handlers.setdefault(event, []).append(handler)
            return handler

        def decorator(fn: AnyHandler) -> AnyHandler:
            self._handlers.setdefault(event, []).append(fn)
            return fn

        return decorator

    def _emit(self, event: str, data: Any = None) -> None:
        for handler in self._handlers.get(event, []):
            try:
                result = handler(data)
                if asyncio.iscoroutine(result):
                    loop = self._loop or asyncio.get_event_loop()
                    loop.create_task(result)
            except Exception as exc:
                logger.error("Error in '%s' handler: %s", event, exc)

    async def connect(self) -> None:
        """Connect to the TikTok LIVE stream.

        For most use cases, prefer :meth:`run` which handles the event loop
        setup automatically. Use ``connect`` directly when integrating with
        an existing async application (FastAPI, aiohttp, etc.)::

            import asyncio
            from tiktok_live_api import TikTokLive

            async def main():
                client = TikTokLive("username", api_key="KEY")
                client.on("chat", lambda e: print(e["comment"]))
                await client.connect()

            asyncio.run(main())
        """
        self._intentional_close = False
        self._loop = asyncio.get_event_loop()
        uri = f"{WS_BASE}?uniqueId={self.unique_id}&apiKey={self.api_key}"

        try:
            self._ws = await websockets.connect(
                uri,
                additional_headers={"User-Agent": f"tiktok-live-api-python/{_VERSION}"},
                ping_interval=10,
                ping_timeout=30,
                close_timeout=5,
            )
        except Exception as exc:
            self._emit("error", {"error": str(exc)})
            raise

        self._connected = True
        self._reconnect_attempts = 0
        self._emit("connected", {"uniqueId": self.unique_id})

        try:
            async for raw in self._ws:
                try:
                    event = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    continue

                self._event_count += 1
                event_type = event.get("event", "unknown")
                data = event.get("data", event)

                self._emit("event", event)
                self._emit(event_type, data)
        except websockets.ConnectionClosed:
            pass
        except Exception as exc:
            self._emit("error", {"error": str(exc)})
        finally:
            self._connected = False
            self._emit("disconnected", {"uniqueId": self.unique_id})

            if (
                not self._intentional_close
                and self.auto_reconnect
                and self._reconnect_attempts < self.max_reconnect_attempts
            ):
                self._reconnect_attempts += 1
                delay = min(2 ** (self._reconnect_attempts - 1), 30)
                logger.info(
                    "Reconnecting in %ds (attempt %d/%d)...",
                    delay,
                    self._reconnect_attempts,
                    self.max_reconnect_attempts,
                )
                await asyncio.sleep(delay)
                await self.connect()

    def disconnect(self) -> None:
        """Disconnect from the stream."""
        self._intentional_close = True
        if self._ws is not None:
            if self._loop is not None and self._loop.is_running():
                self._loop.create_task(self._ws.close())
            else:
                try:
                    asyncio.get_event_loop().run_until_complete(self._ws.close())
                except RuntimeError:
                    pass
        self._connected = False

    def run(self) -> None:
        """Connect and block until disconnected.

        This is the simplest way to use the client. It creates an event loop,
        connects to the stream, and blocks until the stream ends or
        :meth:`disconnect` is called::

            from tiktok_live_api import TikTokLive

            client = TikTokLive("streamer", api_key="KEY")
            client.on("chat", lambda e: print(e["comment"]))
            client.run()
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self.disconnect)
            except (NotImplementedError, ValueError, OSError):
                pass

        try:
            loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            self.disconnect()
        finally:
            loop.close()
