from redis_om import HashModel, Field
from redis_om import get_redis_connection
import datetime

# Assurez-vous de configurer redis_db correctement
redis_db = get_redis_connection(
    host="localhost",
    port=6379,
    db=3,
    decode_responses=True
)

class Student(HashModel):
    name: str = Field(index=True)
    enrolled_courses: list = Field()

    class Meta:
        database = redis_db

class Teacher(HashModel):
    name: str = Field(index=True)
    courses: list = Field()

    class Meta:
        database = redis_db

class Course(HashModel):
    title: str = Field(index=True)
    teacher_id: str = Field(index=True)
    summary: str = Field()
    level: str = Field(index=True)
    available_slots: int = Field()
    student_ids: list = Field()
    expiration_time: datetime.datetime = Field(index=True, default_factory=lambda: datetime.datetime.now() + datetime.timedelta(days=7))

    class Meta:
        database = redis_db