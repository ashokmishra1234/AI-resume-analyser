from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.auth_handler import decode_access_token
from app.services.cache_service import is_token_blacklisted
from app.monitoring.metrics import auth_events_total

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Reject tokens that were explicitly revoked via logout
    if is_token_blacklisted(token):
        auth_events_total.labels(event="token_rejected").inc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please login again."
        )

    payload = decode_access_token(token)
    if payload is None:
        auth_events_total.labels(event="token_rejected").inc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload