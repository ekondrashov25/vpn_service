import asyncio
from backend.db.session import AsyncSessionLocal
from backend.services.cleanup import cleanup_expired_peers


async def main():
    async with AsyncSessionLocal() as session:
        count = await cleanup_expired_peers(session)
        print(f"Removed {count} expired peers")


asyncio.run(main())
