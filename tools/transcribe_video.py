#!/usr/bin/env python3.11
"""
Transcribe YouTube video (no subtitle) via OpenAI Whisper API.
Pipeline: yt-dlp (audio) → compress to mp3 32kbps mono → Whisper API → dedup+filter → save

Usage:
    python3.11 transcribe_video.py <youtube_url_or_id> [--title "Video Title"]
    python3.11 transcribe_video.py QMhUlCoE45Q --title "Sao Thiên Tướng"
    python3.11 transcribe_video.py https://youtu.be/QMhUlCoE45Q

Cost: ~$0.006/min (Whisper API). A 20-min video = ~$0.12
"""

import sys
import os
import re
import subprocess
import tempfile
import argparse
from pathlib import Path

# Load env — try multiple locations
from dotenv import load_dotenv
for _env in [
    Path(__file__).parent.parent.parent.parent.parent / ".env",
    Path.home() / "boitoan_mvps" / ".env",
    Path.home() / "dev" / ".env",
]:
    if _env.exists():
        load_dotenv(_env)
        break

from openai import OpenAI

# ── Config ────────────────────────────────────────────────────────────────────

KEYWORDS = [
    'mệnh','thân','cung','cục','hành','tinh','sao','hóa','lộc','quyền','khoa','kỵ',
    'vượng','hãm','miếu','bình','hạn','đại hạn','tiểu hạn','cách','phú','tử vi',
    'thiên','địa','nhân','phúc','tài','quan','điền','nô','thiên di','phụ mẫu',
    'huynh đệ','phu thê','tử tức','tật ách','đồng','lương','phủ','tướng','liêm',
    'phá','tham','cự','vũ','nhật','nguyệt','sát','cơ','kiếp','không','kình','đà',
    'tuần','triệt','khốc','hư','hồng','đào','long','phượng','thai','tọa','hỏa',
    'linh','quang','quý','khúc','xương','tả','hữu','thiên mã','lộc tồn','văn',
    'âm dương','kim','mộc','thủy','thổ','tí','sửu','dần','mão','thìn','tị',
    'ngọ','mùi','dậu','tuất','hợi','ngũ hành','tứ hóa','chính tinh',
    'phụ tinh','tam hợp','nhị hợp','đối cung','vòng','tràng sinh','thai tuế',
    'đào hoa','thiên hình','thiên diêu','thiên khốc','thiên hư','thiên tài',
    'thiên thọ','phục binh','quan phủ','bạch hổ','tang môn','cô thần','quả tú',
]

OUTPUT_DIR = Path(__file__).parent / "transcripts"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or return as-is if already ID."""
    patterns = [
        r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return url_or_id


def download_audio(video_id: str, out_dir: str) -> str:
    """Download audio as small mp3 (32kbps mono). Returns path to mp3 file."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_template = os.path.join(out_dir, f"{video_id}.%(ext)s")

    cmd = [
        "python3.11", "-m", "yt_dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "32K",          # 32kbps → very small
        "--postprocessor-args", "ffmpeg:-ac 1 -ar 16000",  # mono, 16kHz
        "--output", out_template,
        "--no-playlist",
        url
    ]
    print(f"[1/3] Downloading audio for {video_id}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"yt-dlp error: {result.stderr}")
        raise RuntimeError("Audio download failed")

    mp3_path = os.path.join(out_dir, f"{video_id}.mp3")
    if not os.path.exists(mp3_path):
        # yt-dlp might save with different name
        files = [f for f in os.listdir(out_dir) if f.startswith(video_id)]
        if files:
            mp3_path = os.path.join(out_dir, files[0])
        else:
            raise RuntimeError(f"Audio file not found in {out_dir}")

    size_mb = os.path.getsize(mp3_path) / 1024 / 1024
    print(f"    Audio: {mp3_path} ({size_mb:.1f} MB)")
    return mp3_path


def transcribe_whisper(mp3_path: str, video_id: str) -> str:
    """Send audio to OpenAI Whisper API. Returns full transcript text."""
    client = OpenAI()

    file_size_mb = os.path.getsize(mp3_path) / 1024 / 1024
    print(f"[2/3] Transcribing via Whisper API ({file_size_mb:.1f} MB)...")

    # Whisper API limit: 25MB per file
    if file_size_mb > 24:
        print(f"    File too large ({file_size_mb:.1f}MB), splitting into chunks...")
        return transcribe_chunked(mp3_path, client)

    with open(mp3_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="vi",
            response_format="text"
        )

    duration_min = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", mp3_path],
        capture_output=True, text=True
    ).stdout.strip()
    try:
        cost = float(duration_min) / 60 * 0.006
        print(f"    Duration: {float(duration_min)/60:.1f} min | Cost: ~${cost:.3f}")
    except Exception:
        pass

    return transcript if isinstance(transcript, str) else transcript.text


def transcribe_chunked(mp3_path: str, client: OpenAI, chunk_sec: int = 600) -> str:
    """Split audio into 10-min chunks and transcribe each."""
    import math
    out_dir = os.path.dirname(mp3_path)
    base = os.path.basename(mp3_path).replace(".mp3", "")

    # Get duration
    dur = float(subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", mp3_path],
        capture_output=True, text=True
    ).stdout.strip())

    n_chunks = math.ceil(dur / chunk_sec)
    print(f"    Splitting into {n_chunks} chunks of {chunk_sec//60} min...")

    full_text = []
    for i in range(n_chunks):
        start = i * chunk_sec
        chunk_path = os.path.join(out_dir, f"{base}_chunk{i}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3_path,
            "-ss", str(start), "-t", str(chunk_sec),
            "-ac", "1", "-ar", "16000", "-b:a", "32k",
            chunk_path
        ], capture_output=True)

        with open(chunk_path, "rb") as f:
            t = client.audio.transcriptions.create(
                model="whisper-1", file=f, language="vi", response_format="text"
            )
        full_text.append(t if isinstance(t, str) else t.text)
        os.remove(chunk_path)
        print(f"    Chunk {i+1}/{n_chunks} done")

    return "\n".join(full_text)


def dedup_and_filter(raw_text: str) -> tuple[list[str], list[str]]:
    """Split transcript into sentences, deduplicate, filter by keywords."""
    import re as _re

    # Normalize whitespace
    text = _re.sub(r'\s+', ' ', raw_text).strip()

    # Strategy 1: split on sentence-ending punctuation
    sentences = _re.split(r'(?<=[.!?])\s+', text)

    # If punctuation split produced very few sentences, fall back to word-chunk split
    # (happens when Whisper transcribes without adding periods)
    if len(sentences) < 15 and len(text) > 500:
        # Split by Vietnamese sentence starters + capitalized words every ~15 words
        words = text.split()
        chunk_size = 15
        sentences = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            sentences.append(chunk)

    # Further split long chunks on comma
    expanded = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(s) > 120:
            parts = _re.split(r',\s+', s)
            expanded.extend(p.strip() for p in parts if p.strip())
        else:
            expanded.append(s)

    # Deduplicate (keep order)
    seen = set()
    all_lines = []
    for line in expanded:
        if line and line not in seen:
            seen.add(line)
            all_lines.append(line)

    filtered = [
        l for l in all_lines
        if any(k in l.lower() for k in KEYWORDS)
    ]
    return all_lines, filtered


def save_transcript(video_id: str, title: str, all_lines: list, filtered: list):
    """Save both full and filtered transcripts."""
    # Full transcript
    full_path = OUTPUT_DIR / f"{video_id}_full.txt"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n# Video ID: {video_id}\n\n")
        f.write("\n".join(all_lines))

    # Filtered transcript (tử vi keywords only)
    filtered_path = OUTPUT_DIR / f"{video_id}_filtered.txt"
    with open(filtered_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n# Video ID: {video_id}\n")
        f.write(f"# Total lines: {len(all_lines)}, Filtered: {len(filtered)}\n\n")
        f.write("\n".join(filtered))

    print(f"[3/3] Saved:")
    print(f"    Full:     {full_path} ({len(all_lines)} lines)")
    print(f"    Filtered: {filtered_path} ({len(filtered)} lines)")
    return str(filtered_path)


# ── Main ──────────────────────────────────────────────────────────────────────

def transcribe_video(url_or_id: str, title: str = "") -> str:
    """Full pipeline. Returns path to filtered transcript."""
    video_id = extract_video_id(url_or_id)
    if not title:
        title = video_id

    with tempfile.TemporaryDirectory() as tmp_dir:
        mp3_path = download_audio(video_id, tmp_dir)
        raw_text = transcribe_whisper(mp3_path, video_id)

    all_lines, filtered = dedup_and_filter(raw_text)
    filtered_path = save_transcript(video_id, title, all_lines, filtered)

    print(f"\nDone. Read filtered transcript at:\n  {filtered_path}")
    return filtered_path


def main():
    parser = argparse.ArgumentParser(description="Transcribe YouTube video via Whisper API")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--title", default="", help="Video title (for output file header)")
    args = parser.parse_args()

    transcribe_video(args.url, args.title)


if __name__ == "__main__":
    main()
