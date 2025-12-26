from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

# Password hasher using Argon2id (modern and secure)
ph = PasswordHasher()


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
    jti: str | None = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: The subject of the token (usually user id or email)
        expires_delta: Optional custom expiration time
        jti: Optional JWT ID for token tracking (required for blacklist)

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Add JTI (JWT ID) for token blacklisting support
    if jti:
        to_encode["jti"] = jti
    else:
        to_encode["jti"] = str(uuid.uuid4())
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: str | Any) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        subject: The subject of the token (usually user id or email)

    Returns:
        Encoded JWT refresh token string
    """
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password using Argon2.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against

    Returns:
        True if passwords match, False otherwise
    """
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2id.
    Winner of the Password Hashing Competition.

    Args:
        password: The plain text password to hash

    Returns:
        Hashed password string using Argon2id algorithm
    """
    return ph.hash(password)


# Redis Helper Functions for Security


async def add_token_to_blacklist(jti: str, expires_in: int) -> None:
    """
    Add a token JTI to the blacklist in Redis.

    Args:
        jti: JWT ID (unique identifier for the token)
        expires_in: Seconds until token naturally expires (used as TTL)
    """
    from app.core.redis import get_redis_client
    
    redis = await get_redis_client()
    await redis.setex(f"blacklist:{jti}", expires_in, "revoked")


async def is_token_blacklisted(jti: str) -> bool:
    """
    Check if a token JTI is in the blacklist.

    Args:
        jti: JWT ID to check

    Returns:
        True if token is blacklisted, False otherwise
    """
    from app.core.redis import get_redis_client
    
    redis = await get_redis_client()
    result = await redis.get(f"blacklist:{jti}")
    return result is not None


async def increment_login_attempts(identifier: str) -> int:
    """
    Increment login attempts counter for a user (by email or username).

    Args:
        identifier: User email or username

    Returns:
        Current number of attempts
    """
    from app.core.redis import get_redis_client
    
    redis = await get_redis_client()
    key = f"login_attempts:{identifier}"
    
    # Increment and set expiry if first attempt
    attempts = await redis.incr(key)
    if attempts == 1:
        await redis.expire(key, settings.BLOCK_DURATION_MINUTES * 60)
    
    return attempts


async def reset_login_attempts(identifier: str) -> None:
    """
    Reset login attempts counter for a user.

    Args:
        identifier: User email or username
    """
    from app.core.redis import get_redis_client
    
    redis = await get_redis_client()
    await redis.delete(f"login_attempts:{identifier}")


async def block_user(
    identifier: str, reason: str = "Too many failed login attempts"
) -> None:
    """
    Block a user account temporarily in Redis.

    Args:
        identifier: User email or username
        reason: Reason for blocking
    """
    from app.core.redis import get_redis_client
    import json
    
    redis = await get_redis_client()
    block_data = {
        "identifier": identifier,
        "reason": reason,
        "blocked_at": datetime.now(timezone.utc).isoformat(),
    }
    
    await redis.setex(
        f"user_blocked:{identifier}",
        settings.BLOCK_DURATION_MINUTES * 60,
        json.dumps(block_data)
    )


async def is_user_blocked(identifier: str) -> tuple[bool, dict | None]:
    """
    Check if a user is blocked.

    Args:
        identifier: User email or username

    Returns:
        Tuple of (is_blocked, block_data)
    """
    from app.core.redis import get_redis_client
    import json
    
    redis = await get_redis_client()
    result = await redis.get(f"user_blocked:{identifier}")
    
    if result:
        return True, json.loads(result)
    return False, None


async def unblock_user(identifier: str) -> None:
    """
    Unblock a user account manually (admin action).

    Args:
        identifier: User email or username
    """
    from app.core.redis import get_redis_client
    
    redis = await get_redis_client()
    await redis.delete(f"user_blocked:{identifier}")
    await redis.delete(f"login_attempts:{identifier}")


async def get_all_blocked_users() -> list[dict]:
    """
    Get all currently blocked users (admin function).

    Returns:
        List of block data dictionaries
    """
    from app.core.redis import get_redis_client
    import json
    
    redis = await get_redis_client()
    blocked_users = []
    
    # Scan for all blocked user keys
    async for key in redis.scan_iter("user_blocked:*"):
        data = await redis.get(key)
        if data:
            block_info = json.loads(data)
            # Get TTL (remaining time)
            ttl = await redis.ttl(key)
            block_info["expires_in_seconds"] = ttl
            blocked_users.append(block_info)
    
    return blocked_users
