from polyfactory.factories.pydantic_factory import ModelFactory

from nest.products.core.records import ProductRecord
from nest.products.oda.records import OdaProductDetailRecord
from nest.recipes.core.records import RecipeDetailRecord, RecipeRecord
from nest.recipes.ingredients.records import (
    RecipeIngredientRecord,
)
from nest.recipes.plans.records import RecipePlanRecord
from nest.users.core.records import UserRecord


class UserRecordFactory(ModelFactory[UserRecord]):
    __model__ = UserRecord


class RecipeRecordFactory(ModelFactory[RecipeRecord]):
    __model__ = RecipeRecord


class RecipeDetailRecordFactory(ModelFactory[RecipeDetailRecord]):
    __model__ = RecipeDetailRecord


class RecipeIngredientRecordFactory(ModelFactory[RecipeIngredientRecord]):
    __model__ = RecipeIngredientRecord


class ReipcePlanRecordFactory(ModelFactory[RecipeRecord]):
    __model__ = RecipePlanRecord


class ProductRecordFactory(ModelFactory[ProductRecord]):
    __model__ = ProductRecord


class OdaProductDetailRecordFactory(ModelFactory[OdaProductDetailRecord]):
    __model__ = OdaProductDetailRecord
