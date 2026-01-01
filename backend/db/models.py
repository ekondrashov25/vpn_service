from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from backend.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    peers = relationship("Peer", back_populates="user")


class VPNServer(Base):
    __tablename__ = "vpn_servers"

    id = Column(Integer, primary_key=True)

    country_code = Column(String(8), nullable=False)
    name = Column(String(64), nullable=False)

    endpoint = Column(String(128), nullable=False)
    public_key = Column(String(64), nullable=False)

    subnet = Column(String(32), nullable=False)
    gateway_ip = Column(String(32), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    peers = relationship("Peer", back_populates="server")


class Peer(Base):
    __tablename__ = "peers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("vpn_servers.id"), nullable=False)

    public_key = Column(String(64), nullable=False)
    private_key = Column(String(64), nullable=False)

    ip_address = Column(String(32), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="peers")
    server = relationship("VPNServer", back_populates="peers")

    __table_args__ = (
        UniqueConstraint("server_id", "ip_address", name="uq_peer_ip_per_server"),
    )
