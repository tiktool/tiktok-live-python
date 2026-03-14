"""TikTokCaptions — Real-time AI speech-to-text for TikTok LIVE streams."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
from typing import Any, Callable, Dict, List, Optional, Union

import websockets
import websockets.client

logger = logging.getLogger("tiktok_live_api.captions")

EventHandler = Callable[[Dict[str, Any]], None]
AsyncEventHandler = Callable[[Dict[str, Any]], Any]
AnyHandler = Union[EventHandler, AsyncEventHandler]

CAPTIONS_BASE = "wss://api.tik.tools/captions"
_VERSION = "1.0.1"


class TikTokCaptions:
    """Real-time AI speech-to-text transcription for TikTok LIVE streams.

    This is a unique feature not available in any other TikTok LIVE library.

    Args:
        unique_id: TikTok username (without @).
        api_key: Your TikTool API key. Get one at https://tik.tools
        translate: Target language code for real-time translation (e.g. ``"en"``, ``"es"``).
        diarization: Enable speaker identification (default ``True``).

    Example::

        from tiktok_live_api import TikTokCaptions

        captions = TikTokCaptions("streamer", api_key="KEY", translate="en")

        @captions.on("caption")
        def on_caption(event):
            print(f"[{event.get('speaker', '')}] {event['text']}")

        captions.run()
    """

    def __init__(
        self,
        unique_id: str,
        *,
        api_key: Optional[str] = None,
        translate: Optional[str] = None,
        diarization: bool = True,
    ) -> None:
        self.unique_id = unique_id.lstrip("@")
        self.api_key = api_key or os.environ.get("TIKTOOL_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "api_key is required. Get a free key at https://tik.tools"
            )
        self.translate = translate
        self.diarization = diarization

        self._handlers: Dict[str, List[AnyHandler]] = {}
        self._ws: Optional[websockets.client.WebSocketClientProtocol] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connected = False
        self._intentional_close = False

    @property
    def connected(self) -> bool:
        """Whether the captions client is currently connected."""
        return self._connected

    def on(
        self, event: str, handler: Optional[AnyHandler] = None
    ) -> Any:
        """Register an event handler. Can be used as a decorator or called directly.

        Supported events:
            caption, translation, credits, status, error, connected, disconnected

        Usage as decorator::

            @captions.on("caption")
            def on_caption(event):
                print(event["text"])

        Usage as method::

            captions.on("translation", lambda e: print(e["text"]))
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

    async def start(self) -> None:
        """Start receiving captions from the stream.

        For most use cases, prefer :meth:`run` which handles the event loop
        automatically. Use ``start`` when integrating with an existing
        async application.
        """
        self._intentional_close = False
        self._loop = asyncio.get_event_loop()
        params = f"uniqueId={self.unique_id}&apiKey={self.api_key}"
        if self.translate:
            params += f"&translate={self.translate}"
        if self.diarization:
            params += "&diarization=true"

        uri = f"{CAPTIONS_BASE}?{params}"

        try:
            self._ws = await websockets.connect(
                uri,
                additional_headers={"User-Agent": f"tiktok-live-api-python/{_VERSION}"},
                ping_interval=10,
                ping_timeout=30,
            )
        except Exception as exc:
            self._emit("error", {"error": str(exc)})
            raise

        self._connected = True
        self._emit("connected", {"uniqueId": self.unique_id})

        try:
            async for raw in self._ws:
                try:
                    event = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    continue

                msg_type = event.get("type", "unknown")
                self._emit(msg_type, event)
        except websockets.ConnectionClosed:
            pass
        except Exception as exc:
            self._emit("error", {"error": str(exc)})
        finally:
            self._connected = False
            self._emit("disconnected", {"uniqueId": self.unique_id})

    def stop(self) -> None:
        """Stop receiving captions."""
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
        """Start receiving captions and block until stopped.

        Creates an event loop, connects to the captions stream, and blocks
        until the stream ends or :meth:`stop` is called::

            from tiktok_live_api import TikTokCaptions

            captions = TikTokCaptions("streamer", api_key="KEY", translate="en")
            captions.on("caption", lambda e: print(e["text"]))
            captions.run()
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self.stop)
            except (NotImplementedError, ValueError, OSError):
                pass

        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.stop()
        finally:
            loop.close()
