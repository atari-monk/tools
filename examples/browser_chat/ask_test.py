from browser_chat import (
    default_config,
    browser_connect,
    browser_disconnect,
    chatgpt_create,
    chatgpt_ask,
)



def main():

    config = default_config()


    browser = browser_connect(
        config.browser
    )


    chat = chatgpt_create(
        browser
    )


    answer = chatgpt_ask(
        chat,
        "Explain Docker in 5 sentences."
    )


    print("\nANSWER:\n")
    print(answer)


    browser_disconnect(
        browser
    )



if __name__ == "__main__":
    main()