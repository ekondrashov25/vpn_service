import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://vpn_user:strong_password_here@localhost:5432/vpn_db",
)
