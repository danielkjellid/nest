from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory, T
from nest.products.core.records import ProductRecord
from nest.products.oda.records import OdaProductDetailRecord
from nest.products.oda.tests.utils import get_oda_product_response_dict
from nest.recipes.core.records import RecipeDetailRecord, RecipeRecord
from nest.recipes.ingredients.records import (
    RecipeIngredientItemGroupRecord,
    RecipeIngredientRecord,
)
from nest.users.core.records import UserRecord


class UserRecordFactory(ModelFactory[UserRecord]):
    __model__ = UserRecord


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
