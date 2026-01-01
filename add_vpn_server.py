import asyncio

from backend.db.session import AsyncSessionLocal
from backend.db.models import VPNServer


async def main():
    async with AsyncSessionLocal() as session:
        server = VPNServer(
            country_code="NL",
            name="nl-ams-1",
            endpoint="188.166.11.131:51820",
            public_key="vA/VFSHHwauyus1IUgXE+ukiAg4czgW4xH3XIOSm9WY=",  
            subnet="10.10.0.0/24",
            gateway_ip="10.10.0.1",
            is_active=True,
        )

        session.add(server)
        await session.commit()

        print(f"VPN server added with id={server.id}")


if __name__ == "__main__":
    asyncio.run(main())
