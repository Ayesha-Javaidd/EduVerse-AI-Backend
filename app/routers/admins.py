from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.crud import admins as crud_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

def admin_guard(user):
    if user["role"] != "admin":
        raise HTTPException(403, "Admin only")

# ------------------ SELF PROFILE ------------------

@router.get("/me")
async def get_my_admin_profile(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    return await crud_admin.get_admin_by_user(current_user["user_id"])

# ------------------ DASHBOARD ------------------

@router.get("/teachers")
async def list_teachers(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    teachers = await crud_admin.get_all_teachers()
    return {"total": len(teachers), "teachers": teachers}

@router.get("/students")
async def list_students(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    students = await crud_admin.get_all_students()
    return {"total": len(students), "students": students}

@router.get("/courses")
async def list_courses(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    courses = await crud_admin.get_all_courses()
    return {"total": len(courses), "courses": courses}
