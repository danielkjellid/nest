from polyfactory.factories.pydantic_factory import ModelFactory

from nest.products.core.records import ProductRecord
from nest.products.oda.records import OdaProductDetailRecord
from nest.recipes.core.records import RecipeDetailRecord, RecipeRecord
from nest.recipes.ingredients.records import (
    RecipeIngredientItemGroupRecord,
    RecipeIngredientRecord,
)
from nest.users.core.types import User


class UserRecordFactory(ModelFactory[User]):
    __model__ = User


class RecipeRecordFactory(ModelFactory[RecipeRecord]):
    __model__ = RecipeRecord


class RecipeDetailRecordFactory(ModelFactory[RecipeDetailRecord]):
    __model__ = RecipeDetailRecord


class RecipeIngredientRecordFactory(ModelFactory[RecipeIngredientRecord]):
    __model__ = RecipeIngredientRecord


class RecipeIngredientItemGroupRecordFactory(
    ModelFactory[RecipeIngredientItemGroupRecord]
):
    __model__ = RecipeIngredientItemGroupRecord


class ProductRecordFactory(ModelFactory[ProductRecord]):
    __model__ = ProductRecord


class OdaProductDetailRecordFactory(ModelFactory[OdaProductDetailRecord]):
    __model__ = OdaProductDetailRecord
