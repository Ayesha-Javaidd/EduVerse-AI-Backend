from fastapi import Depends, HTTPException, Header
from app.core.security import decode_token

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Authorization header missing")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    return payload
