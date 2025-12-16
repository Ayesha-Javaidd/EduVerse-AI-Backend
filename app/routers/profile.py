from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.crud import students, teachers, admins, super_admin
from app.schemas.students import StudentUpdate
from app.schemas.teachers import TeacherUpdate
from app.schemas.admins import AdminUpdateRequest
from app.schemas.super_admin import SuperAdminUpdate

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


async def get_profile(user_id: str, role: str):
    if role == "student":
        return await students.get_student_by_user(user_id)
    elif role == "teacher":
        return await teachers.get_teacher_by_user(user_id)
    elif role == "admin":
        return await admins.get_admin_by_user(user_id)
    elif role == "super-admin":
        return await super_admin.get_superadmin_by_user(user_id)
    else:
        raise HTTPException(400, "Unknown role")


UPDATE_SCHEMAS = {
    "student": StudentUpdate,
    "teacher": TeacherUpdate,
    "admin": AdminUpdateRequest,
    "super_admin": SuperAdminUpdate,
}

UPDATE_CRUD = {
    "student": students.update_student_profile,
    "teacher": teachers.update_teacher_profile,
    "admin": admins.update_admin_profile,
    "super_admin": super_admin.update_superadmin,
}
