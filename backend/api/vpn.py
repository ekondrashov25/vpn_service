from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas import VPNCreateRequest, VPNCreateResponse
from backend.db.deps import get_db
from backend.services.peer_service import (
    create_peer, 
    NoAvailableServer,
    NoFreeIP
)
from backend.services.wg_config import generate_wg_config

router = APIRouter(prefix="/vpn", tags=["VPN"])

@router.post("/create", response_model=VPNCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_vpn(payload: VPNCreateRequest, session: AsyncSession = Depends(get_db)):
    try:
        peer = await create_peer(
            session=session, 
            telegram_id=payload.telegram_id,
        )
        
        config = generate_wg_config(peer)
        return {"config": config}
    except NoAvailableServer:
        raise HTTPException(
            status_code=503,
            detail="No VPN servers available",
        )

    except NoFreeIP:
        raise HTTPException(
            status_code=429,
            detail="No free IPs available",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )