import asyncio

from backend.db.session import AsyncSessionLocal
from backend.services.peer_service import create_peer


async def main():
    async with AsyncSessionLocal() as session:
        peer = await create_peer(session, telegram_id=123456)

        print("Peer created:")
        print("IP:", peer.ip_address)
        print("Public key:", peer.public_key)


asyncio.run(main())
