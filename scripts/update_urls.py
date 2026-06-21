#!/usr/bin/env python3
"""
YouTube URL Auto-Updater
========================
Discovers new videos for the creators already listed in transcripts/urls.txt
and appends their URLs under the matching `# Creator` heading.

How it works (no API key, stdlib only):
    1. Parse urls.txt into sections keyed by their `# Creator` header.
    2. For each section, take the first video URL and resolve its YouTube
       channel_id from the watch page.
    3. Fetch that channel's public RSS feed
       (https://www.youtube.com/feeds/videos.xml?channel_id=UC...),
       which lists the latest ~15 uploads.
    4. Append any video IDs not already present in the file, newest at the
       bottom (matching the existing ordering).

Adding a new creator: drop a `# Their Name` heading plus ONE of their video
URLs into urls.txt. The next run discovers the rest automatically.

Usage:
    python scripts/update_urls.py            # update urls.txt in place
    python scripts/update_urls.py --dry-run  # show what would be added
"""

import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TRANSCRIPTS_DIR = SCRIPT_DIR.parent / "transcripts"
URLS_FILE = TRANSCRIPTS_DIR / "urls.txt"
LOG_FILE = TRANSCRIPTS_DIR / ".update_urls.log"

# Collects everything printed this run so it can also be written to LOG_FILE.
# (Lets the scheduled task be a bare `python update_urls.py` with no shell
# redirection — logging is built in and portable.)
_run_log: list[str] = []


def say(msg: str = "") -> None:
    print(msg)
    _run_log.append(msg)


def write_log() -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # On a fresh clone transcripts/ may not exist yet; create it so the first
    # run can write its log instead of crashing on a missing parent dir.
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n===== {stamp} =====\n")
        f.write("\n".join(_run_log) + "\n")

VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})")
CHANNEL_ID_RE = re.compile(r'"(?:channelId|externalChannelId)":"(UC[a-zA-Z0-9_-]{22})"')
FEED_ID_RE = re.compile(r"<yt:videoId>([a-zA-Z0-9_-]{11})</yt:videoId>")


# SOCS/CONSENT cookie skips YouTube's EU consent interstitial, which otherwise
# 302s every request (incl. the Shorts probe below) to consent.youtube.com.
_HEADERS = {"User-Agent": "Mozilla/5.0", "Cookie": "SOCS=CAI; CONSENT=YES+1"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # surface the 3xx instead of following it


_NO_REDIRECT_OPENER = urllib.request.build_opener(_NoRedirect)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def is_short(vid: str) -> bool:
    """True if `vid` is a YouTube Short.

    Probes /shorts/<id>: a real long-form video 30x-redirects to /watch, while
    a Short stays put and returns 200. This pipeline tracks long-form videos
    only (Shorts rarely yield useful transcripts), so discovery drops them.
    On any network error returns False (keep) — a transient failure must never
    silently drop a real upload; a re-probe next run will reclassify it.
    """
    req = urllib.request.Request(f"https://www.youtube.com/shorts/{vid}", headers=_HEADERS)
    try:
        with _NO_REDIRECT_OPENER.open(req, timeout=20) as resp:
            return resp.status == 200
    except Exception:
        return False


def video_id(url: str) -> str | None:
    m = VIDEO_ID_RE.search(url)
    return m.group(1) if m else None


def resolve_channel_id(vid: str) -> str | None:
    """Resolve a video's channel_id from its watch page."""
    try:
        html = fetch(f"https://www.youtube.com/watch?v={vid}")
    except Exception as e:
        say(f"  ! could not fetch watch page for {vid}: {e}")
        return None
    # The channelId/externalChannelId JSON keys are an undocumented detail of
    # YouTube's watch-page markup and can change without notice. Wrap the scrape
    # so a markup change degrades to "skip this creator" instead of crashing the
    # whole run; the next run retries automatically.
    try:
        m = CHANNEL_ID_RE.search(html)
    except Exception as e:
        say(f"  ! channel-id scrape failed for {vid} (YouTube markup change?): {e}")
        return None
    if not m:
        say(f"  ! no channel id found in watch page for {vid} (YouTube markup change?)")
    return m.group(1) if m else None


def latest_video_ids(channel_id: str) -> list[str]:
    """Return latest video IDs from a channel's RSS feed (newest first)."""
    try:
        xml = fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    except Exception as e:
        say(f"  ! could not fetch RSS for {channel_id}: {e}")
        return []
    return FEED_ID_RE.findall(xml)


def main() -> int:
    dry_run = "--dry-run" in sys.argv

    if not URLS_FILE.exists():
        say(f"Not found: {URLS_FILE}")
        write_log()
        return 1

    lines = URLS_FILE.read_text(encoding="utf-8").splitlines()

    # All video IDs already in the file (for global dedup).
    existing_ids = {vid for ln in lines if (vid := video_id(ln))}

    # Find section header line numbers. A creator header is a `#` line that
    # starts a section: in urls.txt every `# Creator` heading is preceded by a
    # blank line (or sits at the top of the file). Requiring that blank-line
    # boundary stops an inline `#` comment placed *between* a creator's URLs
    # from being mistaken for a new header and splitting the section (which
    # would append discovered URLs under the wrong creator). The top
    # "instructions" comments have no URLs under them, so they're filtered out
    # later by the per-section video-ID check.
    headers: list[tuple[int, str]] = []
    for i, ln in enumerate(lines):
        if not ln.strip().startswith("#"):
            continue
        prev_blank = i == 0 or not lines[i - 1].strip()
        if not prev_blank:
            continue  # inline/comment line within a section, not a header
        headers.append((i, ln.strip().lstrip("#").strip()))

    # Insertions keyed by the line index to insert *after* (end of section).
    insertions: dict[int, list[str]] = {}
    total_new = 0

    for idx, (header_line, name) in enumerate(headers):
        section_start = header_line + 1
        section_end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        section_lines = lines[section_start:section_end]
        section_ids = [vid for ln in section_lines if (vid := video_id(ln))]

        if not section_ids:
            continue  # not a creator section (e.g. the instructions header)

        say(f"[{name}]")
        channel_id = resolve_channel_id(section_ids[0])
        if not channel_id:
            say("  ! could not resolve channel; skipping")
            continue

        feed_ids = latest_video_ids(channel_id)
        new_ids = [v for v in feed_ids if v not in existing_ids]
        if not new_ids:
            say("  up to date")
            continue

        # Drop Shorts — long-form videos only. Skipped Shorts never enter the
        # file, so they're re-probed each run (cheap: one request each, and the
        # latest-15 RSS window holds few new IDs).
        filtered = []
        for v in new_ids:
            if is_short(v):
                say(f"  - skip short {v}")
            else:
                filtered.append(v)
        new_ids = filtered
        if not new_ids:
            say("  up to date (new uploads were all Shorts)")
            continue

        # Feed is newest-first; reverse so the newest ends up at the bottom,
        # matching the existing file ordering.
        new_urls = [f"https://www.youtube.com/watch?v={v}" for v in reversed(new_ids)]

        # Insert at the end of the section's URL block (after the last
        # non-blank line in the section, before any trailing blank lines).
        last_content = section_start
        for j in range(section_start, section_end):
            if lines[j].strip():
                last_content = j
        insertions.setdefault(last_content, []).extend(new_urls)
        existing_ids.update(new_ids)
        total_new += len(new_ids)

        for u in new_urls:
            say(f"  + {u}")

    if total_new == 0:
        say("\nNothing new.")
        write_log()
        return 0

    if dry_run:
        say(f"\n[dry-run] would add {total_new} URL(s).")
        write_log()
        return 0

    # Rebuild the file with insertions applied.
    out: list[str] = []
    for i, ln in enumerate(lines):
        out.append(ln)
        if i in insertions:
            out.extend(insertions[i])
    URLS_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    say(f"\nAdded {total_new} URL(s) to {URLS_FILE.name}.")
    write_log()
    return 0


if __name__ == "__main__":
    sys.exit(main())
