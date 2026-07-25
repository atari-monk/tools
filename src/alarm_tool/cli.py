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

    content = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
    header = f"## {date_string()}"

    if header in content:
        return

    with LOG_FILE.open("a", encoding="utf-8") as file:
        if content and not content.endswith("\n"):
            file.write("\n")
        if content:
            file.write("\n")
        file.write(f"{header}\n\n")


def append_log(description: str) -> None:
    ensure_date_header()

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"- {description}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI timer with alarm")
    parser.add_argument(
        "-t",
        "--time",
        required=True,
        help="Examples: 30, 45s, 90sec, 2m, 5min",
    )
    parser.add_argument(
        "-d",
        "--description",
        required=True,
        help="Work description",
    )

    args = parser.parse_args()

    duration = parse_duration(args.time)

    if duration <= 0:
        raise SystemExit("Time must be greater than zero.")

    append_log(args.description.strip())

    countdown(duration)

    threading.Thread(target=play_alarm, daemon=True).start()
    show_alert()


if __name__ == "__main__":
    main()