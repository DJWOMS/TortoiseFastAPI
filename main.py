from typing import List
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
import crud
import schemas
from models import UserPydantic, User, UserInPydantic, UserPydanticList, Item, ItemPydantic

app = FastAPI()


@app.post('/')
async def get_schemas():
    print(f"{UserPydantic.schema()}\n{'*'*20}")
    user = await User.create(email="e@e.com", hashed_password="123456", is_active=True)
    user_schema = await UserInPydantic.from_tortoise_orm(user)
    print(user_schema.json())
    return user_schema.json()


@app.post('/test_create')
async def create_users():
    await User.create(email="e4@e.com", hashed_password="123456", is_active=True)
    await User.create(email="e2@e.com", hashed_password="123456", is_active=False)
    await User.create(email="e3@e.com", hashed_password="123456", is_active=True)
    user_schema = await UserPydanticList.from_queryset(User.all())
    print(user_schema.dict())
    print(user_schema.json())
    return user_schema.json()


@app.get("/", response_model=UserPydantic)
async def get_users_list():
    users = await UserPydantic.from_queryset_single(User.get(id=3))
    print(users.json())
    return users


@app.get("/users", response_model=List[UserPydantic])
async def get_users():
    return await UserPydantic.from_queryset(User.all())


@app.post("/users", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)


@app.get(
    "/user/{user_id}", response_model=UserPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@app.post(
    "/user/{user_id}", response_model=UserPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserInPydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@app.delete("/user/{user_id}", response_model=schemas.Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return schemas.Status(message=f"Deleted user {user_id}")


register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["models"], "aerich.models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
