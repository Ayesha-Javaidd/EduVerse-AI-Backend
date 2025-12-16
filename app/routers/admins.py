from fastapi import APIRouter, Depends, HTTPException
from app.schemas.admins import AdminUpdateRequest, AdminResponse
from app.crud import admins as crud_admin
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/me", response_model=AdminResponse)
async def get_my_admin_profile(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not an admin")

    admin = await crud_admin.get_admin_by_user(current_user["user_id"])
    if not admin:
        raise HTTPException(404, "Admin profile not found")

    return admin


@router.patch("/me", response_model=AdminResponse)
async def update_my_admin_profile(
    update: AdminUpdateRequest, current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not an admin")

    return await crud_admin.update_admin_profile(
        current_user["user_id"], update.dict(exclude_unset=True)
    )
