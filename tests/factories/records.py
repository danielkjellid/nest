from polyfactory.factories.pydantic_factory import ModelFactory

from nest.products.core.records import ProductRecord


class ProductRecordFactory(ModelFactory[ProductRecord]):
    __model__ = ProductRecord
