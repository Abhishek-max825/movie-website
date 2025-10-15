import asyncio
from contextlib import suppress

from .services.cleanup import sweep_old_content


async def start_cleanup_loop() -> None:
    # Run periodic cleanup every 10 minutes
    while True:
        with suppress(Exception):
            sweep_old_content()
        await asyncio.sleep(600)


