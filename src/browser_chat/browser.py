from playwright.sync_api import sync_playwright

from .types import BrowserState

from .config import BrowserConfig


def browser_connect(
    config: BrowserConfig
) -> BrowserState:

    playwright = (
        sync_playwright()
        .start()
    )


    browser = (
        playwright.chromium
        .connect_over_cdp(
            config.cdp_url
        )
    )


    if not browser.contexts:
        raise RuntimeError(
            "Chrome has no contexts"
        )


    context = browser.contexts[0]


    return BrowserState(
        playwright=playwright,
        browser=browser,
        context=context,
    )



def browser_disconnect(
    state: BrowserState
):

    if not state.connected:
        return


    state.browser.close()

    state.playwright.stop()

    state.connected = False