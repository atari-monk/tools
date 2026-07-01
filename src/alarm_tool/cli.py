import argparse
import subprocess
import threading
import time


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


def countdown(seconds: int) -> None:
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rRemaining: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
        seconds -= 1

    print("\rRemaining: 00:00")


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


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI timer with alarm")
    parser.add_argument("time", help="Examples: 30, 45s, 90sec, 2m, 5min")
    args = parser.parse_args()

    duration = parse_duration(args.time)

    if duration <= 0:
        raise SystemExit("Time must be greater than zero.")

    countdown(duration)

    threading.Thread(target=play_alarm, daemon=True).start()
    show_alert()


if __name__ == "__main__":
    main()