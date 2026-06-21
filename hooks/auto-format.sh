#!/bin/bash
# Auto-format hook (PostToolUse on Write/Edit): formats the edited file in place
# with whatever formatter is available — ruff for .py, prettier for JS/TS/CSS.
# Makes no assumption about project layout (no `cd backend`/`cd frontend`) and is
# tool-guarded, so it's a safe no-op in projects without those formatters.
# Always exits 0 — formatting must never block an edit.

FILE_PATH="$CLAUDE_FILE_PATH"
if [ -z "$FILE_PATH" ]; then
  # Claude Code delivers the hook payload as JSON on stdin; fall back to it when
  # the env var isn't set. Prefer python3, but fall back to `python` (Windows
  # often ships only `python`).
  PY_JSON='import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))'
  if command -v python3 >/dev/null 2>&1; then
    FILE_PATH=$(python3 -c "$PY_JSON" 2>/dev/null)
  elif command -v python >/dev/null 2>&1; then
    FILE_PATH=$(python -c "$PY_JSON" 2>/dev/null)
  fi
fi

# Nothing to do if we couldn't resolve a real file.
[ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ] || exit 0

# Run a formatter, swallowing its output but logging a one-line warning to
# stderr if it fails. We still exit 0 overall (formatting must never block an
# edit), but a misconfigured/broken formatter is now diagnosable instead of
# silently doing nothing.
run_fmt() {
  if ! "$@" >/dev/null 2>&1; then
    echo "auto-format: formatter failed: $* (file: $FILE_PATH)" >&2
  fi
}

case "$FILE_PATH" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      run_fmt ruff format "$FILE_PATH"
    elif command -v uv >/dev/null 2>&1; then
      run_fmt uv run ruff format "$FILE_PATH"
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.css)
    if command -v prettier >/dev/null 2>&1; then
      run_fmt prettier --write "$FILE_PATH"
    elif command -v npx >/dev/null 2>&1; then
      run_fmt npx --no-install prettier --write "$FILE_PATH"
    fi
    ;;
esac

exit 0
