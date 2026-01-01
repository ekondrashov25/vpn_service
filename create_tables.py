import asyncio

from backend.db.session import engine
from backend.db.base import Base
from backend.db import models


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
