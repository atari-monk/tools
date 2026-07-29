import time

from playwright.sync_api import BrowserContext, Locator, Page

from .selectors import (
    ASSISTANT_MESSAGES,
    TEXTBOXES,
)


def find_chatgpt_page(context: BrowserContext) -> Page:
    for page in context.pages:
        if "chatgpt.com" in page.url:
            return page

    page = context.new_page()

    page.goto(
        "https://chatgpt.com"
    )

    return page


def find_textbox(page: Page) -> Locator:
    for selector in TEXTBOXES:
        locator = page.locator(
            selector
        )

        count = locator.count()

        if count == 0:
            continue

        for i in range(count):
            element = locator.nth(i)

            if element.is_visible():
                return element

    raise RuntimeError(
        "Could not find visible ChatGPT textbox"
    )


def wait_for_chat_ready(page: Page) -> None:
    find_textbox(page)


def assistant_count(page: Page) -> int:
    return page.locator(
        ASSISTANT_MESSAGES
    ).count()


def get_last_assistant(page: Page) -> str:
    message = page.locator(
        ASSISTANT_MESSAGES
    ).last

    for _ in range(30):
        text = message.inner_text()

        if text.strip():
            return text

        time.sleep(1)

    raise RuntimeError(
        "Assistant message was empty"
    )