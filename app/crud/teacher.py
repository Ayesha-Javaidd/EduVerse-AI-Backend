from app.db.database import db
from datetime import datetime
from app.schemas.teacher import TeacherCreate

from bson import ObjectId

async def create_teacher(teacher : TeacherCreate):
    teacher_dict = teacher.dict()
    if not teacher_dict["tenant_id"]:
        teacher_dict["tenant_id"] = ObjectId()

    teacher_dict.update(
        {
            "assignedCourses" :[],
            "createdAt" : datetime.utcnow,
            "updatedAt" : datetime.utcnow
        }
    )

    result = await db.teachers.insert_one(teacher_dict)
    new_teacher = await db.tecahers.find_one({"id" : result.inserted_id})
    new_teacher["id"] = str( new_teacher["id"])
    new_teacher["tenant_id"] = str( new_teacher["tenant_id"])
    return new_teacher