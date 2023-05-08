import pytest

from nest.audit_logs.selectors import (
    get_log_entries_for_instance,
    get_log_entries_for_object,
)
from nest.audit_logs.tests.utils import create_log_entry
from nest.products.models import Product
from nest.products.tests.utils import create_product
from nest.users.models import User
from nest.users.tests.utils import create_user

pytestmark = pytest.mark.django_db


class TestAuditLogsSelectors:
    def test_get_log_entries_for_object(self, django_assert_num_queries):
        """
        Test that the get_log_entries_for_object selector returns correct output within
        query limits.
        """
        author = create_user()
        product = create_product()
        create_log_entry(
            instance=product, user=author, changes={"name": ("Old name", "New name")}
        )
        create_log_entry(
            instance=product,
            user=author,
            changes={"supplier": ("Old supplier", "New supplier")},
        )

        with django_assert_num_queries(1):
            log_entries = get_log_entries_for_object(model=Product, pk=product.id)

        with django_assert_num_queries(2):
            no_log_entries = get_log_entries_for_object(model=User, pk=author.id)

        assert len(log_entries) == 2
        assert len(no_log_entries) == 0

    def test_get_log_entries_for_instance(self, django_assert_num_queries):
        """
        Test that the get_log_entries_for_instance selector returns correct output within
        query limits.
        """
        author = create_user()
        product = create_product()
        create_log_entry(
            instance=product, user=author, changes={"name": ("Old name", "New name")}
        )
        create_log_entry(
            instance=product,
            user=author,
            changes={"supplier": ("Old supplier", "New supplier")},
        )

        with django_assert_num_queries(1):
            log_entries = get_log_entries_for_instance(instance=product)

        with django_assert_num_queries(2):
            no_log_entries = get_log_entries_for_instance(instance=author)

        assert len(log_entries) == 2
        assert len(no_log_entries) == 0
