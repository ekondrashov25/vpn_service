import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.db.session import AsyncSessionLocal
from backend.db.models import Peer
from backend.services.wg_config import generate_wg_config


async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
        select(Peer)
        .options(selectinload(Peer.server))
        .order_by(Peer.id.desc())
        .limit(1)
        )   
        peer = result.scalar_one()

        conf = generate_wg_config(peer)
        print(conf)


asyncio.run(main())
