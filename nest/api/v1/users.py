from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from sqlalchemy import select
import asyncio
from nest.models import UserModel, UserSchema
from nest.database import session, Transactional, offline_session
from nest.database.sessions import db

users_router = InferringRouter()


@cbv(users_router)
class UsersApi:
    class TestOutput(BaseModel):
        id: int

    @users_router.get("/")
    async def test(self) -> TestOutput:
        query = select(UserSchema)
        res = await session.execute(query)
        print(res.scalars().all())
        return self.TestOutput(id=1)

    class UserCreateInput(BaseModel):
        email: str
        first_name: str
        last_name: str
        password: str

    @users_router.post("/create/", response_model=None)
    async def create(self, payload: UserCreateInput) -> None:
        session.add(
            UserSchema(
                email=payload.email,
                first_name=payload.first_name,
                last_name=payload.last_name,
                password=payload.password,
            )
        )
        await session.commit()
        # await db.commit()
