from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
import jwt

from app.core.config import settings
from app.core.database import get_session
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    is_user_blocked,
    increment_login_attempts,
    reset_login_attempts,
    block_user,
    add_token_to_blacklist,
)
from app.models.user import User
from app.schemas.token import (
    TokenWithRefresh,
    RefreshTokenRequest,
    TokenPayload,
)
from app.api.deps import CurrentUser, TokenDep

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenWithRefresh)
async def login(
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenWithRefresh:
    """
    OAuth2 compatible token login with refresh token.

    Get access and refresh tokens for future requests using
    username/email and password.
    Account will be blocked after 5 failed attempts within 5 minutes.
    """
    identifier = form_data.username  # Can be username or email
    
    # Check if user is blocked
    blocked, block_data = await is_user_blocked(identifier)
    if blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Account temporarily blocked. "
                f"Reason: {block_data.get('reason', 'Security')}. "
                f"Try again later."
            ),
        )
    
    # Try to find user by username or email
    user = session.exec(
        select(User).where(
            (User.username == identifier) | (User.email == identifier)
        )
    ).first()

    if not user:
        # Increment failed attempts even if user doesn't exist
        # (to prevent enumeration)
        await increment_login_attempts(identifier)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        # Increment failed login attempts
        attempts = await increment_login_attempts(identifier)
        
        # Block user if max attempts reached
        if attempts >= settings.MAX_LOGIN_ATTEMPTS:
            await block_user(
                identifier,
                reason=f"Too many failed login attempts ({attempts})",
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Account blocked due to {attempts} failed login "
                    f"attempts. Try again in "
                    f"{settings.BLOCK_DURATION_MINUTES} minutes."
                ),
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                f"Incorrect username or password. Attempts remaining: "
                f"{settings.MAX_LOGIN_ATTEMPTS - attempts}"
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Reset login attempts on successful login
    await reset_login_attempts(identifier)
    
    # Create access and refresh tokens
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.id)

    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout(current_user: CurrentUser, token: TokenDep) -> dict:
    """
    Logout the current user by blacklisting the JWT token.

    The token will be added to a Redis blacklist and cannot be reused.
    """
    try:
        # Decode token to get JTI and expiration
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        jti = payload.get("jti")
        exp = payload.get("exp")
        
        if not jti or not exp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token format"
            )
        
        # Calculate remaining TTL
        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        ttl = int((expires_at - now).total_seconds())
        
        if ttl > 0:
            # Add to blacklist with TTL
            await add_token_to_blacklist(jti, ttl)
        
        return {
            "message": "Successfully logged out",
            "username": current_user.username
        }
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


@router.post("/refresh", response_model=TokenWithRefresh)
async def refresh_token(
    session: Annotated[Session, Depends(get_session)],
    refresh_request: RefreshTokenRequest,
) -> TokenWithRefresh:
    """
    Refresh access token using a valid refresh token.

    Returns a new access token and refresh token.
    """
    try:
        # Decode refresh token
        payload = jwt.decode(
            refresh_request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # Verify it's a refresh token
        if token_data.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        user_id = int(token_data.sub)
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create new tokens
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        new_refresh_token = create_refresh_token(subject=user.id)
        
        return TokenWithRefresh(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=dict)
def get_current_user_info(current_user: CurrentUser) -> dict:
    """
    Get current authenticated user information.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }
