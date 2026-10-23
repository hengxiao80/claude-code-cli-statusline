# claude-code-cli-statusline

A right-aligned status line for the Claude Code CLI:

```
Opus 5.5 | ctx 15% | $2.43 | 5h 8% (↻ 20:50) | 7d 27% (↻ Fri 21:00)
```

| Cell | Meaning |
| --- | --- |
| `Opus 5.5` | current model |
| `ctx 15%` | share of the context window used |
| `$2.43` | API-price estimate of the session's tokens since it started (same as `/cost`); not billed on a subscription plan |
| `5h 8% (↻ 20:50)` | 5-hour usage limit used, and when it resets (local time) |
| `7d 27% (↻ Fri 21:00)` | weekly usage limit used, and when it resets |

Cells whose data Claude Code does not send are left out (the usage limits appear only on subscription plans).

## Install

```bash
git clone <this repo> ~/claude-code-cli-statusline
~/claude-code-cli-statusline/install.sh
```

`install.sh` links `~/.claude/statusline.py` to the copy in the repo (an existing file there is kept as
`statusline.py.bak`) and adds the `statusLine` entry to `~/.claude/settings.json`, leaving other settings alone.
To update later, `git pull`; nothing needs reinstalling.

Needs Python 3 (`/usr/bin/python3`, else `python3` on the PATH). No other dependencies.

## Notes

- Right alignment: Claude Code does not pass the terminal width, so the script reads it from `/dev/tty`
  (falling back to `$COLUMNS`). Claude Code trims leading spaces, so the padding starts with U+2800
  (braille blank), which is invisible but not whitespace. The line ends 4 columns short of the edge
  (`pad = width - len(line) - 4`); change the 4 if it doesn't line up in your terminal.
- Each run saves its input to `~/.claude/statusline-last.json`, which shows the fields Claude Code
  sends. It stays in `~/.claude`, outside this repo.
- To remove: delete the `statusLine` entry from `~/.claude/settings.json`.
