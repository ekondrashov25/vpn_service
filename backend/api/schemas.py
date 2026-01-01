from pydantic import BaseModel


class VPNCreateRequest(BaseModel):
    telegram_id: int


class VPNCreateResponse(BaseModel):
    config: str
