import time

from threading import Lock

from playwright.sync_api import Page

from .types import BrowserState, ChatState

from .dom import find_textbox

from .dom import (
    find_chatgpt_page,
    wait_for_chat_ready,
    assistant_count,
    get_last_assistant,
)

from .selectors import STOP_GENERATING


def chatgpt_create(browser: BrowserState) -> ChatState:
    page = find_chatgpt_page(
        browser.context
    )

    wait_for_chat_ready(
        page
    )

    return ChatState(
        browser=browser,
        page=page,
        lock=Lock(),
    )


def clear_input(chat: ChatState) -> None:
    textbox = find_textbox(chat.page)

    textbox.click()

    textbox.press(
        "Control+A"
    )

    textbox.press(
        "Backspace"
    )


def send_message(
    chat: ChatState,
    prompt: str,
) -> int:
    before = assistant_count(
        chat.page
    )

    textbox = find_textbox(chat.page)

    textbox.fill(
        prompt
    )

    textbox.press(
        "Enter"
    )

    return before


def wait_for_response(
    chat: ChatState,
    previous_count: int,
) -> None:
    chat.page.wait_for_function(
        """
        previous => {

            return document.querySelectorAll(
              "[data-message-author-role='assistant']"
            ).length > previous;

        }
        """,
        arg=previous_count,
        timeout=120000
    )


def wait_until_finished(chat: ChatState) -> None:
    assistant = chat.page.locator(
        "[data-message-author-role='assistant']"
    ).last

    timeout = time.time() + 120

    last_text = ""

    stable_count = 0

    while time.time() < timeout:
        try:
            text = assistant.inner_text(
                timeout=5000
            )
        except Exception:
            text = ""

        if len(text.strip()) == 0:
            stable_count = 0
            time.sleep(0.5)
            continue

        if text == last_text:
            stable_count += 1
        else:
            stable_count = 0
            last_text = text

        if stable_count >= 4:
            return

        time.sleep(0.5)

    raise TimeoutError(
        "Assistant response did not finish"
    )


def wait_until_generation_stops(page: Page) -> None:
    timeout = time.time() + 120

    while time.time() < timeout:
        if page.locator(
            STOP_GENERATING
        ).count() == 0:
            return

        time.sleep(0.5)

    raise TimeoutError(
        "Generation did not stop"
    )


def chatgpt_ask(
    chat: ChatState,
    prompt: str,
) -> str:
    with chat.lock:
        wait_for_chat_ready(
            chat.page
        )

        clear_input(
            chat
        )

        before = send_message(
            chat,
            prompt
        )

        wait_for_response(
            chat,
            before
        )

        wait_until_generation_stops(
            chat.page
        )

        wait_until_finished(
            chat
        )

        chat.messages_sent += 1

        return get_last_assistant(
            chat.page
        )