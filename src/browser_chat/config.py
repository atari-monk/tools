from dataclasses import dataclass


@dataclass
class BrowserConfig:
    cdp_url: str = "http://localhost:9222"
    headless: bool = False
    timeout_ms: int = 30000


@dataclass
class AgentConfig:
    max_messages_per_chat: int = 50
    response_timeout: int = 120
    retry_count: int = 3


@dataclass
class Config:
    browser: BrowserConfig
    agent: AgentConfig


def default_config() -> Config:
    return Config(
        browser=BrowserConfig(),
        agent=AgentConfig(),
    )