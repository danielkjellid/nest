from nest.tests.conftest import DBStatementCounter
from nest.database import session
from nest.models import User
import pytest
from sqlalchemy import select

pytestmark = pytest.mark.asyncio


async def test_y(async_session):

    # async with session.begin() as conn:
    #     with DBStatementCounter(session) as ctr:
    #         conn.add(
    #             User(first_name="Example", last_name="Example", email="test@test.com")
    #         )
    #         conn.commit()
    #         print(ctr.count)
    #
    # await session.dispose()

    async_session.add(
        User(first_name="Example", last_name="Example", email="test@test.com")
    )
    await async_session.commit()

    statement = select(User).where(User.first_name == "Example")
    user = await async_session.execute(statement=statement)
    u = user.scalar_one()

    u1 = await async_session.get(User, 1)
    print(u1)
    print("----")

    print(
        u.id,
    )

    assert False
