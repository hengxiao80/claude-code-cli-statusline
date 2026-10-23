#!/usr/bin/env bash
# Install the status line on this machine:
#   - link ~/.claude/statusline.py to the copy in this repo (so `git pull` updates it)
#   - add the statusLine entry to ~/.claude/settings.json, keeping all other settings
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
claude_dir="$HOME/.claude"
target="$claude_dir/statusline.py"
settings="$claude_dir/settings.json"

# Python 3: prefer /usr/bin/python3, else whatever python3 is on PATH.
if [ -x /usr/bin/python3 ]; then
    py=/usr/bin/python3
elif command -v python3 >/dev/null 2>&1; then
    py="$(command -v python3)"
else
    echo "install.sh: no python3 found" >&2
    exit 1
fi

mkdir -p "$claude_dir"

# Link the script, backing up a real file that is already there.
if [ -e "$target" ] && [ ! -L "$target" ]; then
    mv "$target" "$target.bak"
    echo "Backed up existing $target to $target.bak"
fi
ln -sfn "$repo/statusline.py" "$target"
echo "Linked $target -> $repo/statusline.py"

# Add or replace the statusLine entry.
"$py" - "$settings" "$py" "$target" <<'EOF'
import json
import os
import sys

path, py, script = sys.argv[1:4]
settings = {}
if os.path.exists(path):
    with open(path) as f:
        settings = json.load(f)
settings["statusLine"] = {"type": "command", "command": "%s %s" % (py, script)}
with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")
print("Set statusLine in %s: %s" % (path, settings["statusLine"]["command"]))
EOF

echo "Done. The status line appears after your next message in Claude Code."
