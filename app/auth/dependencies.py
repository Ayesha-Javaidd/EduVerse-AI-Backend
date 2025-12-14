# from bson import ObjectId
# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from app.db.database import db

# from app.utils.security import decode_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = decode_token(token)
#     user = await db.users.find_one({"_id": ObjectId(payload["user_id"]), "status": "active"})
#     if not user:
#         raise HTTPException(401, "User not found or inactive")
#     return {
#         "id": str(user["_id"]),
#         "role": user["role"],
#         "tenantId": user.get("tenantId")
#     }


from fastapi import Depends
from app.auth.router import oauth2_scheme
from app.db.database import db
from app.utils.security import decode_token
from bson import ObjectId
from fastapi import HTTPException


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user = await db.users.find_one(
        {"_id": ObjectId(payload["user_id"]), "status": "active"}
    )
    if not user:
        raise HTTPException(401, "User not found or inactive")
    return {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "tenantId": user.get("tenantId"),
    }
