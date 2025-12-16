from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.crud.profile import UPDATE_CRUD, UPDATE_SCHEMAS, get_profile

router = APIRouter(prefix="", tags=["Profile"])


@router.get("/me")
async def get_my_profile(current_user=Depends(get_current_user)):
    profile = await get_profile(current_user["user_id"], current_user["role"])
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@router.patch("/me")
async def update_my_profile(request_body: dict, current_user=Depends(get_current_user)):
    role = current_user["role"]
    schema_cls = UPDATE_SCHEMAS[role]
    updates = schema_cls(**request_body).dict(exclude_unset=True)

    updated_profile = await UPDATE_CRUD[role](current_user["user_id"], updates)
    if not updated_profile:
        raise HTTPException(404, "Profile not found")
    return updated_profile
