from fastapi import APIRouter, HTTPException, Depends
from app.crud.quiz_submissions import get_teacher_dashboard
from app.schemas.teachers import TeacherUpdate, TeacherResponse
from app.crud.teachers import get_teacher_by_user, update_teacher_profile
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/me", response_model=TeacherResponse)
async def get_my_teacher_profile(current_user=Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(403, "Not a teacher")

    teacher = await get_teacher_by_user(current_user["user_id"])
    if not teacher:
        raise HTTPException(404, "Teacher profile not found")

    return teacher


@router.patch("/me", response_model=TeacherResponse)
async def update_my_teacher_profile(
    updates: TeacherUpdate, current_user=Depends(get_current_user)
):
    if current_user["role"] != "teacher":
        raise HTTPException(403, "Not a teacher")

    return await update_teacher_profile(
        current_user["user_id"], updates.dict(exclude_unset=True)
    )


@router.get("/me/dashboard")
async def my_dashboard(current_user=Depends(get_current_user)):
    return await get_teacher_dashboard(current_user["user_id"])


@router.get("/me/students")
async def my_students(current_user=Depends(get_current_user)):
    return await get_teacher_students(current_user["user_id"])
