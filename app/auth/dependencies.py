# from fastapi import Depends, HTTPException, Header

# from app.utils.security import decode_token


# def get_current_user(authorization: str = Header(None)):
#     if not authorization:
#         raise HTTPException(401, "Authorization header missing")

#     token = authorization.replace("Bearer ", "")
#     payload = decode_token(token)
#     return payload



from fastapi import Depends, HTTPException, Header
from app.utils.security import decode_token
from app.db.database import db
from bson import ObjectId

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Authorization header missing")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    user = await db.users.find_one({
        "_id": ObjectId(payload["user_id"]),
        "status": "active"
    })

    if not user:
        raise HTTPException(401, "User not found or inactive")

    return {
        "id": str(user["_id"]),
        "role": user["role"],
        "tenantId": user.get("tenantId")
    }


def require_roles(*roles):
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(403, "Access forbidden")
        return current_user
    return role_checker
