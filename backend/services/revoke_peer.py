from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Peer
from backend.wg.peers import remove_peer


class PeerNotFound(Exception):
    pass


async def revoke_peer(
    session: AsyncSession,
    peer_id: int,
):
    result = await session.execute(
        select(Peer).where(
            Peer.id == peer_id,
            Peer.is_active == True
        )
    )
    peer = result.scalar_one_or_none()

    if peer is None:
        raise PeerNotFound("Peer not found or already inactive")

    remove_peer(peer.public_key)

    peer.is_active = False
    await session.commit()

    return peer
