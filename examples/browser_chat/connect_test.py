from browser_chat import (
    default_config,
    browser_connect,
    browser_disconnect,
)


def main():

    config = default_config()


    browser = browser_connect(
        config.browser
    )


    print(
        "Connected:",
        browser.connected
    )


    print(
        "Pages:",
        len(
            browser.context.pages
        )
    )


    browser_disconnect(
        browser
    )



if __name__ == "__main__":
    main()