# Alarm tool log feature

Simplify the alarm tool. Remove all of the interactive "plan" / "done" workflow. The alarm should only keep a minimal log.

## Console output

Keep the current console output that prints timestamps.

Example:

```text
alarm 25m
start: 2026-07-25 10:00:00
...
stop: 2026-07-25 10:25:00
```

Do **not** ask for a "done" summary after the timer finishes.

## Log file

Use:

```
/home/atari-monk/atari-monk/project/dev-notes/en/alarm-log.md
```

When the alarm starts:

* Ask once:

  * `What are you going to work on?`
* Save the answer.
* Create the log file if it does not exist.
* Append a date heading only if it does not already exist:

```md
## yyyy-mm-dd
```

Then append one bullet for the Pomodoro:

```md
- Pomodoro 1 — Short description
```

The description is simply the user's answer.

Example:

```md
## 2026-07-25

- Pomodoro 1 — Fix alarm logging
- Pomodoro 2 — Review pull request
- Pomodoro 3 — Write documentation
```

Pomodoro numbering restarts each day and should increment based on the number of Pomodoro entries already present under that day's heading.

The log should contain **only** these bullet entries. Do not store:

* start timestamps
* stop timestamps
* alarm duration
* "plan"
* "done"

Those belong only in the console output.

The goal is to keep the implementation extremely simple and make the log useful as a daily history of completed Pomodoros instead of a verbose session record.