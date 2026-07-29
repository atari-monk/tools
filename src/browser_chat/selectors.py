TEXTBOXES = [

    # Current ChatGPT textarea
    "textarea[placeholder='Ask anything']",

    # Older versions
    "textarea[name='prompt-textarea']",

    # Contenteditable fallback
    "[contenteditable='true']",

]


ASSISTANT_MESSAGES = (
    "[data-message-author-role='assistant']"
)


USER_MESSAGES = (
    "[data-message-author-role='user']"
)


STOP_GENERATING = (
    "button[aria-label*='Stop']"
)


CONTINUE_GENERATING = (
    "button:has-text('Continue generating')"
)


NEW_CHAT = (
    "a[href='/']"
)


FILE_INPUT = (
    "input[type='file']"
)