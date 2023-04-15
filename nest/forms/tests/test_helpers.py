from dataclasses import dataclass

from pydantic import BaseModel

from nest.forms.helpers import (
    get_inner_list_type,
    is_list,
    is_pydantic_model,
    unwrap_item_type_from_list,
)


class MyModel(BaseModel):
    val: int


@dataclass(frozen=True)
class MyDataclass:
    val: int


class TestFormHelpers:
    def test_is_list(self):
        """
        Test that the is_list helper correctly outputs when a type annotation is a list.
        """

        assert is_list(obj=list[MyModel]) is True
        assert is_list(obj=list[MyDataclass]) is True

        assert is_list(obj=tuple[MyModel]) is False
        assert is_list(obj=tuple[MyDataclass]) is False

        assert is_list(obj=set[MyModel]) is False
        assert is_list(obj=set[MyDataclass]) is False

    def test_is_pydantic_model(self):
        """
        Test that the is_pydantic_model helper correctly outputs when a type annotation
        is a pydantic model.
        """

        assert is_pydantic_model(obj=MyModel) is True
        assert is_pydantic_model(obj=MyDataclass) is False

    def test_get_inner_list_type(self):
        """
        Test that the get_inner_list_type helper correctly retrieves the inner type
        when both a list and the type is passed.
        """

        class_type, is_in_list = get_inner_list_type(obj=MyModel)
        assert class_type is MyModel
        assert is_in_list is False

        class_type, is_in_list = get_inner_list_type(obj=list[MyModel])
        assert class_type is MyModel
        assert is_in_list is True

        class_type, is_in_list = get_inner_list_type(obj=MyDataclass)
        assert class_type is MyDataclass
        assert is_in_list is False

        class_type, is_in_list = get_inner_list_type(obj=list[MyDataclass])
        assert class_type is MyDataclass
        assert is_in_list is True

    def test_unwrap_item_type_from_list(self):
        """
        Test that the unwrap_item_type_from_list helper correctly retrieves the inner
        type from a passed list of types.
        """

        assert unwrap_item_type_from_list(obj=list[MyModel]) == MyModel
        assert unwrap_item_type_from_list(obj=list[int]) == int
        assert unwrap_item_type_from_list(obj=list[MyDataclass]) == MyDataclass
