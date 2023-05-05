import pytest
from nest.core.services import update_model


class TestCoreServices:
    def test_model_update_does_nothing(self, django_assert_num_queries):
        assert False

    def test_model_update_updates_only_passed_fields_from_data(self):
        assert False

    def test_model_update_raises_error_when_called_with_non_existing_field(self):
        assert False

    def test_model_update_updates_many_to_many_field(self):
        assert False

    def test_model_update_standard_and_many_to_many_fields(self):
        assert False

    def test_model_update_sets_automatically_updated_at(self):
        assert False
