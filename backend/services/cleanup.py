from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Peer
from backend.wg.peers import remove_peer


async def cleanup_expired_peers(session: AsyncSession):
    now = datetime.now(timezone.utc)

    result = await session.execute(
        select(Peer).where(
            Peer.is_active == True,
            Peer.expires_at != None,
            Peer.expires_at < now,
        )
    )

    peers = result.scalars().all()

    for peer in peers:
        remove_peer(peer.public_key)
        peer.is_active = False

    await session.commit()

    return len(peers)
