"""Lean, network-free tests for the pure helpers in the transcript pipeline.

This is a config repo, not a library, so these tests deliberately cover only the
parsing / slugifying / due-gating logic that's easy to break and annoying to
debug in production. Anything that touches the network is out of scope.

Run: uv run pytest tests/  (or: python -m pytest tests/)
"""

import sys
from pathlib import Path

import pytest

# The pipeline scripts live in scripts/ and import each other by bare name, so
# put that dir on sys.path before importing them.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import fetch_transcripts  # noqa: E402
import run_pipeline  # noqa: E402


# --- fetch_transcripts.extract_video_id ------------------------------------

@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),  # bare 11-char id
    ],
)
def test_extract_video_id_valid(url, expected):
    assert fetch_transcripts.extract_video_id(url) == expected


def test_extract_video_id_invalid_raises():
    with pytest.raises(ValueError):
        fetch_transcripts.extract_video_id("https://example.com/not-a-video")


# --- fetch_transcripts.slugify_title ---------------------------------------

def test_slugify_basic():
    assert fetch_transcripts.slugify_title("Hello World!") == "hello-world"


def test_slugify_collapses_and_trims_separators():
    assert fetch_transcripts.slugify_title("  A  --  B  ") == "a-b"


def test_slugify_truncates_to_80_chars():
    slug = fetch_transcripts.slugify_title("word " * 100)
    assert len(slug) <= 80


def test_slugify_empty_when_no_alnum():
    assert fetch_transcripts.slugify_title("!!!???") == ""


# --- fetch_transcripts.md_escape (guards the index/ledger) -----------------

def test_md_escape_handles_breaking_chars():
    out = fetch_transcripts.md_escape("a|b]c)d")
    assert "|" not in out.replace("\\|", "")
    assert "\\|" in out and "\\]" in out and "\\)" in out


def test_md_escape_flattens_newlines():
    assert "\n" not in fetch_transcripts.md_escape("line1\nline2")


# --- run_pipeline due-gating -----------------------------------------------

def test_is_due_when_never_run(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: None)
    assert run_pipeline._is_due(force=False) is True


def test_is_due_force_bypasses_gate(monkeypatch):
    # Even if it ran 1 minute ago, --force runs.
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 0.02)
    assert run_pipeline._is_due(force=True) is True


def test_not_due_when_recent(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 1.0)
    monkeypatch.setattr(run_pipeline, "MIN_HOURS_BETWEEN_RUNS", 24.0)
    assert run_pipeline._is_due(force=False) is False


def test_due_when_past_window(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 25.0)
    monkeypatch.setattr(run_pipeline, "MIN_HOURS_BETWEEN_RUNS", 24.0)
    assert run_pipeline._is_due(force=False) is True


def test_hours_since_last_run_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(run_pipeline, "STATE_FILE", tmp_path / "nope")
    assert run_pipeline._hours_since_last_run() is None


def test_hours_since_last_run_reads_timestamp(tmp_path, monkeypatch):
    from datetime import datetime, timedelta

    state = tmp_path / ".last_run"
    state.write_text((datetime.now() - timedelta(hours=5)).isoformat())
    monkeypatch.setattr(run_pipeline, "STATE_FILE", state)
    elapsed = run_pipeline._hours_since_last_run()
    assert elapsed is not None
    assert 4.5 < elapsed < 5.5


def test_hours_since_last_run_corrupt_file(tmp_path, monkeypatch):
    state = tmp_path / ".last_run"
    state.write_text("not-a-timestamp")
    monkeypatch.setattr(run_pipeline, "STATE_FILE", state)
    assert run_pipeline._hours_since_last_run() is None
