#!/bin/bash
# Auto-format hook (PostToolUse on Write/Edit): formats the edited file in place
# with whatever formatter is available — ruff for .py, prettier for JS/TS/CSS.
# Makes no assumption about project layout (no `cd backend`/`cd frontend`) and is
# tool-guarded, so it's a safe no-op in projects without those formatters.
# Always exits 0 — formatting must never block an edit.

FILE_PATH="$CLAUDE_FILE_PATH"
if [ -z "$FILE_PATH" ]; then
  # Claude Code delivers the hook payload as JSON on stdin; fall back to it when
  # the env var isn't set.
  FILE_PATH=$(python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
fi

# Nothing to do if we couldn't resolve a real file.
[ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ] || exit 0

case "$FILE_PATH" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format "$FILE_PATH" >/dev/null 2>&1
    elif command -v uv >/dev/null 2>&1; then
      uv run ruff format "$FILE_PATH" >/dev/null 2>&1
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.css)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write "$FILE_PATH" >/dev/null 2>&1
    elif command -v npx >/dev/null 2>&1; then
      npx --no-install prettier --write "$FILE_PATH" >/dev/null 2>&1
    fi
    ;;
esac

exit 0
