from fastapi import APIRouter, Depends, HTTPException
from app.schemas.students import StudentUpdate, StudentResponse
from app.crud import students as crud_student
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(require_role("student"))],
)


@router.get("/me", response_model=StudentResponse)
async def get_my_profile(
    current_user=Depends(get_current_user),
):
    student = await crud_student.get_student_by_user(current_user["user_id"])
    if not student:
        raise HTTPException(404, "Student profile not found")

    return student


@router.patch("/me", response_model=StudentResponse)
async def update_my_profile(
    update: StudentUpdate,
    current_user=Depends(get_current_user),
):
    updated_student = await crud_student.update_student_profile(
        current_user["user_id"],
        update.dict(exclude_unset=True),
    )

    if not updated_student:
        raise HTTPException(404, "Student profile not found")

    return updated_student
