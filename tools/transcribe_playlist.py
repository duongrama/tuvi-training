#!/usr/bin/env python3.11
"""
Batch transcribe all videos in a YouTube playlist that DON'T have VI subtitles.
Skips videos that already have subtitles (uses yt-dlp to check first).

Usage:
    python3.11 transcribe_playlist.py <playlist_url>
    python3.11 transcribe_playlist.py --only-missing  # skip already-transcribed
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

from dotenv import load_dotenv
for _env in [
    Path(__file__).parent.parent.parent.parent.parent / ".env",
    Path.home() / "boitoan_mvps" / ".env",
    Path.home() / "dev" / ".env",
]:
    if _env.exists():
        load_dotenv(_env)
        break

from transcribe_video import transcribe_video, extract_video_id, OUTPUT_DIR

def get_playlist_videos(playlist_url: str) -> list[tuple[str, str]]:
    """Returns list of (video_id, title) from playlist."""
    result = subprocess.run(
        ["python3.11", "-m", "yt_dlp", "--flat-playlist",
         "--print", "%(id)s|%(title)s", playlist_url],
        capture_output=True, text=True
    )
    videos = []
    for line in result.stdout.strip().splitlines():
        if "|" in line:
            vid_id, title = line.split("|", 1)
            videos.append((vid_id.strip(), title.strip()))
    return videos


def has_vi_subtitle(video_id: str) -> bool:
    """Check if video has Vietnamese auto-subtitles."""
    result = subprocess.run(
        ["python3.11", "-m", "yt_dlp",
         "--list-subs", f"https://www.youtube.com/watch?v={video_id}"],
        capture_output=True, text=True, timeout=30
    )
    return "vi" in result.stdout


def already_transcribed(video_id: str) -> bool:
    """Check if we already have a transcript for this video."""
    return (OUTPUT_DIR / f"{video_id}_filtered.txt").exists()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_url", help="YouTube playlist URL")
    parser.add_argument("--only-missing", action="store_true",
                        help="Skip videos that already have VI subtitles")
    parser.add_argument("--skip-done", action="store_true", default=True,
                        help="Skip videos already transcribed (default: True)")
    args = parser.parse_args()

    print(f"Fetching playlist: {args.playlist_url}")
    videos = get_playlist_videos(args.playlist_url)
    print(f"Found {len(videos)} videos\n")

    to_process = []
    skipped_sub = []
    skipped_done = []

    for vid_id, title in videos:
        if args.skip_done and already_transcribed(vid_id):
            skipped_done.append((vid_id, title))
            continue
        if args.only_missing and has_vi_subtitle(vid_id):
            skipped_sub.append((vid_id, title))
            continue
        to_process.append((vid_id, title))

    print(f"To process:    {len(to_process)}")
    print(f"Already done:  {len(skipped_done)}")
    print(f"Has VI sub:    {len(skipped_sub)}")
    print()

    failed = []
    for i, (vid_id, title) in enumerate(to_process, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(to_process)}] {title}")
        print(f"    ID: {vid_id}")
        print('='*60)
        try:
            transcribe_video(vid_id, title)
        except Exception as e:
            print(f"    ERROR: {e}")
            failed.append((vid_id, title, str(e)))

    print(f"\n\n{'='*60}")
    print(f"DONE: {len(to_process) - len(failed)} success, {len(failed)} failed")
    if failed:
        print("\nFailed:")
        for vid_id, title, err in failed:
            print(f"  {vid_id} | {title}: {err}")


if __name__ == "__main__":
    main()
