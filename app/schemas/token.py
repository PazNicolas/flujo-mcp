from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenWithRefresh(BaseModel):
    """Token response with refresh token."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str | None = None
    jti: str | None = None
    type: str | None = None
