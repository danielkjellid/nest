from nest.api.v1.users import user_router


@user_router.get("/")
async def user_list_api():
    return await {"Test": "user"}
