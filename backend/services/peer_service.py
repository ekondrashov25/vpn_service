from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from backend.db.models import User, VPNServer, Peer
from backend.wg.keys import generate_keypair
from backend.wg.peers import add_peer
from backend.ipam.allocator import allocate_ip


class NoAvailableServer(Exception):
    pass    


class NoFreeIP(Exception):
    pass


async def create_peer(session: AsyncSession, telegram_id: int) -> Peer:
    """
    Создаёт VPN peer для пользователя.
    1 user = 1 active peer
    """
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.flush()  

    result = await session.execute(
        select(Peer)
        .where(
            Peer.user_id == user.id,
            Peer.is_active == True
        )
        .options(selectinload(Peer.server))
    )

    existing_peer = result.scalar_one_or_none()

    if existing_peer:
        return existing_peer

    result = await session.execute(
        select(VPNServer)
        .where(VPNServer.is_active == True)
        .order_by(VPNServer.id)
        .limit(1)
    )

    server = result.scalar_one_or_none()

    if server is None:
        raise NoAvailableServer("No active VPN servers available")

    result = await session.execute(
        select(Peer.ip_address)
        .where(
            Peer.server_id == server.id,
            Peer.is_active == True,
        )
    )
    used_ips = {row[0] for row in result.all()}
    
    print("USED IPS:", used_ips)
    print("SUBNET:", server.subnet)
    print("GATEWAY:", server.gateway_ip)


    try:
        ip_address = allocate_ip(
            subnet=server.subnet,
            used_ips=used_ips,
            reserved_ips={server.gateway_ip},
        )
    except RuntimeError:
        raise NoFreeIP("No free IPs on server")

    private_key, public_key = generate_keypair()

    peer = Peer(
        user_id=user.id,
        server_id=server.id,
        public_key=public_key,
        private_key=private_key,
        ip_address=ip_address,
        is_active=True,
    )

    session.add(peer)

    try:
        await session.flush()
    except IntegrityError:
        raise NoFreeIP("IP allocation race condition")

    add_peer(
        public_key=public_key,
        allowed_ips=ip_address,
    )
    await session.commit()

    result = await session.execute(
        select(Peer)
        .options(selectinload(Peer.server))
        .where(Peer.id == peer.id)
    )
    peer = result.scalar_one()

    return peer
