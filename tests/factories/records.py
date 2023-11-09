from polyfactory.factories.pydantic_factory import ModelFactory

from nest.products.core.records import ProductRecord
from nest.recipes.core.records import RecipeDetailRecord, RecipeRecord
from nest.users.core.records import UserRecord


class UserRecordFactory(ModelFactory[UserRecord]):
    __model__ = UserRecord


class RecipeRecordFactory(ModelFactory[RecipeRecord]):
    __model__ = RecipeRecord


class RecipeDetailRecordFactory(ModelFactory[RecipeDetailRecord]):
    __model__ = RecipeDetailRecord


class ProductRecordFactory(ModelFactory[ProductRecord]):
    __model__ = ProductRecord
