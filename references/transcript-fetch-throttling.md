# Transcript fetch throttling — tuning notes & backlog

How `scripts/fetch_transcripts.py` stays under YouTube's per-IP anti-bot
throttle, and the ranked options for when it isn't enough. Researched 2026-06-20.

## Context

The fetcher uses `youtube-transcript-api`, which scrapes YouTube's **unofficial**
`timedtext` (caption) endpoint — there is **no official API key or documented
quota**. The constraint is YouTube's undocumented **per-IP throttling**, surfaced
as `RequestBlocked` / `IpBlocked`. Key facts:

- Each video ≈ **4 requests** (one watch-page GET for metadata + the library's 3
  internal calls). So an unspaced run of N videos fires ~4N requests in a tight
  burst — and **the burst is what trips the throttle**, not the daily total.
- A **residential home IP is the best case**; cloud/datacenter IPs get blocked on
  request #1 by ASN reputation. **Never route this through a cloud host.**
- The caption endpoint got **much stricter and fingerprint-sensitive in mid-2025**.
- No published threshold exists. The most reliable number is this IP's own
  observed ceiling: **~30 *unspaced* fetches before blocking**.
- Sub-daily cadence is a known trap for this IP: running every 3h kept it "warm"
  and the throttle never cleared. **Daily runs let the per-IP window reset.**

## Current settings (applied 2026-06-20)

- `MAX_TRANSCRIPTS_PER_RUN = 40` (was 25).
- Randomised **4–8s gap before each networked fetch** (`FETCH_SLEEP_MIN/MAX`),
  jittered because a fixed cadence is itself a fingerprint. Spreads a run over
  minutes so it no longer bursts — 40 spaced is gentler than the old unspaced 25.
- Daily cadence unchanged; 3-strike circuit breaker stops a run if blocks recur
  (≈ a 24h backoff, which is the correct response to a flag).
- Error handling already matches the library taxonomy: `RequestBlocked`/
  `IpBlocked`/`YouTubeRequestFailed` retry next run; `TranscriptsDisabled`/
  `NoTranscriptFound`/`VideoUnavailable`/`PoTokenRequired` are permanent skips
  recorded in `no-transcript-available.md`.

## Conditional backlog — apply based on results

**Decision rule:** watch the "Blocked (throttled…)" count in `transcripts/.pipeline.log`
over a few daily runs. **~0–1/run → do nothing.** **≥3/run (breaker tripping early)
→ escalate down this list.**

1. **Measure first (default).** This IP's own behaviour beats the low-confidence
   public numbers. Don't change anything until the data says to.
2. **TLS/browser impersonation via `curl_cffi`** — the clearest firsthand throttle
   mitigation found (the caption endpoint fingerprints the TLS handshake). The
   `_TimeoutSession` wrapper already isolates the HTTP client, so swap the
   `requests.Session` for a `curl_cffi` session with `impersonate="chrome"`. New
   dep. **Apply only if blocks recur.**
3. **Consent cookie on `fetch_page_metadata`** (data-quality, throttle-independent)
   — it uses bare `urllib` with no consent cookie and sometimes mislabels videos
   as `unknown-creator/`; add `Cookie: SOCS=CAI; CONSENT=YES+1` (same fix already
   in `update_urls.py`). One line, zero risk. **Do anytime.**
4. **Webshare free rotating-residential proxy** (speed escape hatch) — natively
   supported via `WebshareProxyConfig` (`retries_when_blocked` default 10); free
   1 GB tier likely covers a whole backlog (transcripts are tiny), drains in one
   run, home IP untouched. Needs a signup + a gitignored secret. **Only if daily
   cadence is too slow.**

## Explicitly skipped (with reasons)

- **Dead retry path** (`TRANSCRIPT_RETRIES=1` → the in-fetch retry never fires) —
  harmless; next-run retry already covers blocked videos.
- **Deduping the redundant watch-page fetch** — ~25% fewer requests, but only to
  the lightly-throttled *page* endpoint, not the caption endpoint. Low payoff.
- **Cookie auth** — broken upstream in the library.
- **Official YouTube Data API v3** — a dead end: `captions.download` only works
  for videos the authenticated user **owns**, useless for third-party channels.
