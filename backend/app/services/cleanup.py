import os
import shutil
import time
from pathlib import Path
from typing import Optional

from ..config import settings


def get_movie_dir(movie_id: str) -> Path:
    return Path(settings.temp_dir) / settings.hls_dirname / movie_id


def delete_movie_dir(movie_id: str) -> bool:
    target = get_movie_dir(movie_id)
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
        return True
    return False


def sweep_old_content(now: Optional[float] = None) -> int:
    """Delete HLS directories older than cleanup_after_seconds.

    Returns count of deleted directories.
    """
    if now is None:
        now = time.time()
    root = Path(settings.temp_dir) / settings.hls_dirname
    if not root.exists():
        return 0
    deleted = 0
    for child in root.iterdir():
        if not child.is_dir():
            continue
        try:
            mtime = child.stat().st_mtime
            if now - mtime > settings.cleanup_after_seconds:
                shutil.rmtree(child, ignore_errors=True)
                deleted += 1
        except OSError:
            continue
    return deleted


