import os
import shutil
import subprocess
import uuid
from pathlib import Path

from ..config import settings


def generate_movie_id() -> str:
    return uuid.uuid4().hex


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def convert_to_hls(input_path: str, movie_id: str) -> str:
    """Convert a local video file to HLS into temp/hls/{movie_id}/index.m3u8.

    Returns the directory path containing the HLS output.
    """
    hls_root = os.path.join(settings.temp_dir, settings.hls_dirname)
    output_dir = os.path.join(hls_root, movie_id)
    ensure_dir(output_dir)

    # Single-variant HLS for compliance; can extend to ladder later
    output_manifest = os.path.join(output_dir, "index.m3u8")

    # Basic, broadly compatible HLS settings
    # Segment length 6s, independent segments, no list size limit
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-preset",
        "veryfast",
        "-movflags",
        "+faststart",
        "-profile:v",
        "baseline",
        "-level",
        "3.0",
        "-start_number",
        "0",
        "-hls_time",
        "6",
        "-hls_list_size",
        "0",
        "-hls_playlist_type",
        "vod",
        "-f",
        "hls",
        output_manifest,
    ]

    completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        # Clean partial outputs on failure
        with contextlib.suppress(Exception):
            shutil.rmtree(output_dir, ignore_errors=True)
        raise RuntimeError(f"FFmpeg failed: {completed.stderr[:500]}")

    return output_dir


