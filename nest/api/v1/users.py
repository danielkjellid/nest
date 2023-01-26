from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel

users_router = InferringRouter()


@cbv(users_router)
class UsersApi:
    class TestOutput(BaseModel):
        id: int

    @users_router.get("/")
    def test(self) -> TestOutput:
        return self.TestOutput(id=1)
