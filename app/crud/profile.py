from fastapi import HTTPException
from app.crud import super_admin, teachers, admins, students
from app.schemas.admins import AdminUpdateRequest
from app.schemas.students import StudentUpdate
from app.schemas.super_admin import SuperAdminUpdate
from app.schemas.teachers import TeacherUpdate


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
