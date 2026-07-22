import argparse
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/atari-monk/atari-monk/project/dev-notes/en/alarm-log.md")


def parse_duration(value: str) -> int:
    value = value.strip().lower()

    if value.endswith("min"):
        return int(float(value[:-3]) * 60)
    if value.endswith("m"):
        return int(float(value[:-1]) * 60)
    if value.endswith("sec"):
        return int(float(value[:-3]))
    if value.endswith("s"):
        return int(float(value[:-1]))

    return int(float(value))


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def countdown(seconds: int) -> None:
    print(f"start: {timestamp()}")

    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rRemaining: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
        seconds -= 1

    print("\rRemaining: 00:00")
    print(f"stop: {timestamp()}")


def play_alarm() -> None:
    sound = "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"

    while True:
        subprocess.run(
            ["paplay", sound],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        time.sleep(0.2)


def show_alert() -> None:
    subprocess.run(
        [
            "notify-send",
            "--urgency=critical",
            "⏰ Timer Finished",
            "Time is up!",
        ],
        check=False,
    )

    subprocess.run(
        [
            "zenity",
            "--warning",
            "--title=Timer Finished",
            "--text=Time is up!",
        ],
        check=False,
    )


def ensure_date_header() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if LOG_FILE.exists():
        content = LOG_FILE.read_text(encoding="utf-8")
    else:
        content = ""

    header = f"## {date_string()}"

    if header in content:
        return

    with LOG_FILE.open("a", encoding="utf-8") as f:
        if content and not content.endswith("\n"):
            f.write("\n")
        if content:
            f.write("\n")
        f.write(f"{header}\n\n")


def next_pomodoro_number() -> int:
    content = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""

    header = f"## {date_string()}"
    if header not in content:
        return 1

    section = content.split(header, 1)[1]
    section = section.split("\n## ", 1)[0]

    count = 0
    for line in section.splitlines():
        if line.startswith("- Pomodoro "):
            count += 1

    return count + 1


def append_pomodoro(description: str) -> None:
    ensure_date_header()

    number = next_pomodoro_number()

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- Pomodoro {number} — {description}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI timer with alarm")
    parser.add_argument("time", help="Examples: 30, 45s, 90sec, 2m, 5min")
    args = parser.parse_args()

    duration = parse_duration(args.time)

    if duration <= 0:
        raise SystemExit("Time must be greater than zero.")

    description = input("What are you going to work on? ").strip()
    append_pomodoro(description)

    countdown(duration)

    threading.Thread(target=play_alarm, daemon=True).start()
    show_alert()


if __name__ == "__main__":
    main()