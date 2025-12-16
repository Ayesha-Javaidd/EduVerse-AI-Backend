from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user, require_role
from app.schemas.super_admin import SuperAdminResponse, SuperAdminUpdate
from app.crud.super_admin import get_superadmin_by_user, update_superadmin

router = APIRouter(
    prefix="/super-admin",
    tags=["Super Admin"],
    dependencies=[Depends(require_role("super-admin"))],
)


@router.get("/me", response_model=SuperAdminResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    if current_user["role"] != "super_admin":  # match role in DB
        raise HTTPException(403, "Not a Super Admin")

    super_admin = await get_superadmin_by_user(current_user["user_id"])
    if not super_admin:
        raise HTTPException(404, "Super Admin profile not found")

    return super_admin


@router.patch("/me", response_model=SuperAdminResponse)
async def update_my_profile(
    update: SuperAdminUpdate, current_user=Depends(get_current_user)
):
    if current_user["role"] != "super_admin":
        raise HTTPException(403, "Not a Super Admin")

    updated = await update_superadmin(
        current_user["user_id"], update.dict(exclude_unset=True)
    )

    if not updated:
        raise HTTPException(404, "Super Admin profile not found")

    return updated
