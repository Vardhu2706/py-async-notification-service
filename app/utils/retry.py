# Retry

# Imports 
import asyncio

async def retry(func, *args, retries=3, delay=1, notif_id=None):
    """
    Retry a notification multiple times with delay in case of failure.
    Logs each retry attempt. Supports optional notif_id for traceable logs.
    """
    for attempt in range(retries):
        try:
            return await func(*args)
        except Exception as e:
            prefix = f"[{notif_id}] " if notif_id else ""
            print(f"{prefix}❌ Retry {attempt}/{retries} failed: {e}")
            await asyncio.sleep(delay)
    raise Exception("All retries failed")