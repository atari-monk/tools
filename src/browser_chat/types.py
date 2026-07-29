from dataclasses import dataclass, field

from threading import Lock

from typing import Optional

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
)


@dataclass
class BrowserState:

    playwright: Playwright

    browser: Browser

    context: BrowserContext

    connected: bool = True


@dataclass
class ChatState:

    browser: BrowserState

    page: Page

    lock: Lock = field(
        default_factory=Lock
    )

    messages_sent: int = 0

    current_chat_id: Optional[str] = None