from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.crud import admin_dashboard as crud_admin
from app.utils.guards import admin_guard

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/teachers")
async def list_teachers(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    teachers = await crud_admin.get_all_teachers()
    return {"total": len(teachers), "teachers": teachers}


@router.get("/students")
async def list_students(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    students = await crud_admin.get_all_students(current_user["tenantId"])
    return {"total": len(students), "students": students}


@router.get("/courses")
async def list_courses(current_user=Depends(get_current_user)):
    admin_guard(current_user)
    courses = await crud_admin.get_all_courses()
    return {"total": len(courses), "courses": courses}
