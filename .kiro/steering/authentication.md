# Authentication Guidelines

## Stack

- JWT (JSON Web Tokens) for authentication
- Access token + Refresh token pattern
- python-jose for JWT encoding/decoding
- passlib for password hashing

## Token Configuration

```python
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")  # Required, no default
JWT_ALGORITHM = "HS256"
```

## Token Structure

### Access Token (short-lived)
- Expires: 15 minutes
- Contains: user_id, email, roles
- Used for: API requests

### Refresh Token (long-lived)
- Expires: 7 days
- Contains: user_id, token_type
- Used for: Getting new access tokens
- Stored: HttpOnly cookie or secure storage

## Authentication Flow

```
1. Login: POST /auth/login → {access_token, refresh_token}
2. API Request: Authorization: Bearer {access_token}
3. Token Expired: POST /auth/refresh → {new_access_token}
4. Logout: POST /auth/logout → Invalidate refresh token
```

## FastAPI Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Validate JWT and return current user."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

## Protected Endpoint

```python
@router.get("/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile. Requires authentication."""
    return current_user
```
