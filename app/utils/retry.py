# Retry

# Imports 
import asyncio

async def retry(fn, *args, retries=3, delay=2, **kwargs):
    for attempt in range(retries):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            print(f"❌ Retry {attempt+1}/{retries} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise