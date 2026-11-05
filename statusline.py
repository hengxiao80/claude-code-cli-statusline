#!/usr/bin/python3
# Claude Code status line: model | context used | session cost | plan usage limits.
# Reads the session JSON on stdin. Missing fields are skipped, so it degrades gracefully.
import json
import os
import sys
import time

raw = sys.stdin.read()
try:
    d = json.loads(raw)
except ValueError:
    print("statusline: bad JSON")
    sys.exit(0)

# Keep the last input for debugging which fields are available.
try:
    with open(os.path.expanduser("~/.claude/statusline-last.json"), "w") as f:
        f.write(raw)
except OSError:
    pass


def get(*keys):
    v = d
    for k in keys:
        if not isinstance(v, dict) or k not in v:
            return None
        v = v[k]
    return v


parts = []

model = get("model", "display_name")
if model:
    # Effort level (low ... max) next to the model
    effort = get("effort", "level")
    parts.append("%s (%s)" % (model, effort) if effort else model)

# Context window
pct = get("context_window", "used_percentage")
if pct is not None:
    parts.append("ctx %d%%" % round(pct))

# Session cost (API-equivalent)
cost = get("cost", "total_cost_usd")
if cost is not None:
    parts.append("$%.2f" % cost)

# Subscription usage limits (5-hour and weekly windows)
for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
    used = get("rate_limits", key, "used_percentage")
    if used is not None:
        s = "%s %d%%" % (label, round(used))
        resets = get("rate_limits", key, "resets_at")
        if resets:
            # 5h window: time only; weekly window: weekday and time
            fmt = "%H:%M" if key == "five_hour" else "%a %H:%M"
            s += " (\u21bb %s)" % time.strftime(fmt, time.localtime(resets))
        parts.append(s)

line = " | ".join(parts)


def term_width():
    # stdout is a pipe, so ask the controlling terminal; fall back to $COLUMNS.
    try:
        fd = os.open("/dev/tty", os.O_RDONLY)
        try:
            return os.get_terminal_size(fd).columns
        finally:
            os.close(fd)
    except OSError:
        pass
    try:
        return int(os.environ.get("COLUMNS", ""))
    except ValueError:
        return 0


# Right-align. Claude Code indents the status line, so leave a small margin.
width = term_width()
# Claude Code trims leading whitespace, so the padding starts with U+2800
# (braille blank: invisible, one column wide, not whitespace).
pad = width - len(line) - 4
out = "\u2800" + " " * (pad - 1) + line if pad > 0 else line
sys.stdout.buffer.write((out + "\n").encode("utf-8"))
