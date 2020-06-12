from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(models.Model):
    """Модель пользователя"""
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=1000)
    is_active = fields.BooleanField(default=True)

    async def save(self, *args, **kwargs) -> None:
        self.hashed_password = "123456"
        await super().save(*args, **kwargs)

    class PydanticMeta:
        exclude = ['hashed_password']


class Item(models.Model):
    """Модель items"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    owner = fields.ForeignKeyField('models.User', related_name='items')

    class PydanticMeta:
        allow_cycles = False


UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserPydanticList = pydantic_queryset_creator(User)

ItemPydantic = pydantic_model_creator(Item, name="Items")
