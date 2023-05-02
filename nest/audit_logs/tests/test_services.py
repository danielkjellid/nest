import pytest
from nest.audit_logs.services import (
    _create_log_entry,
    log_update,
    log_delete,
    log_create,
    AuditLogger,
)
from nest.products.tests.utils import create_product
from nest.users.tests.utils import create_user
from nest.audit_logs.models import LogEntry
from nest.core.tests.utils import create_request

pytestmark = pytest.mark.django_db


class TestAuditLogServices:
    def test_log_create_or_updated(self):
        """
        Test that the log_create_or_updated service correctly creates a log entry with
        action = LogEntry.ACTION_CREATE when a new object is created, and a log entry
        with action = LogEntry.ACTION_UPDATE when an existing object is updated.
        """
        assert False

    def test__create_log_entry(self, django_assert_num_queries):
        """
        Test that the _create_log_entry service correctly creates a log entry with
        passed parameters and within query limits.
        """
        assert False

    def test__create_log_entry_no_changes(self, django_assert_num_queries):
        """
        Test that _create_log_entry service correctly returns early when changes are
        empty.
        """
        product = create_product()

        with django_assert_num_queries(0):
            log_entry = _create_log_entry(
                request=None,
                instance=product,
                user=None,
                changes=None,
                action=LogEntry.ACTION_CREATE,
            )

        assert log_entry is None

    def test__create_log_entry_with_request(self):
        """
        Test that the _create_log_entry service correctly attaches user and request to
        the log entry when applicable.
        """
        assert False

    def test_log_create(self):
        """
        Test that the log_create service correctly creates a log entry with action =
        LogEntry.ACTION_CREATE.
        """
        user = create_user()
        product = create_product(name="Awesome product")
        request = create_request(user=user)

        log_entry = log_create(
            instance=product,
            request=request,
            changes={"name": (product.name, "A new name!")},
        )

        assert log_entry.action == LogEntry.ACTION_CREATE

    def test_log_update(self):
        """
        Test that the log_update service correctly creates a log entry with action =
        LogEntry.ACTION_UPDATE.
        """
        user = create_user()
        product = create_product(name="Awesome product")
        request = create_request(user=user)

        log_entry = log_update(
            instance=product,
            request=request,
            changes={"name": (product.name, "A new name!")},
        )

        assert log_entry.action == LogEntry.ACTION_UPDATE

    def test_log_delete(self):
        """
        Test that the log_update service correctly creates a log entry with action =
        LogEntry.ACTION_DELETE.
        """
        user = create_user()
        product = create_product(name="Awesome product")
        request = create_request(user=user)

        log_entry = log_delete(
            instance=product,
            request=request,
            changes={"name": (product.name, None)},
        )

        assert log_entry.action == LogEntry.ACTION_DELETE

    def test_auditlogger_context_manager(self):
        """
        Test that the AuditLogger context manager behaves as expected and creates a
        sensible diff when used.
        """
        product = create_product(name="Awesome product")

        with AuditLogger(instance=product) as audit_logger:
            product.name = "An even more awesome product"
            product.save()

        assert audit_logger.diff == {
            "name": ("Awesome product", "An even more awesome product")
        }
        assert LogEntry.objects.count() == 1
        assert LogEntry.objects.first().changes == {
            "name": ["Awesome product", "An even more awesome product"]
        }

    def test_auditlogger_context_manager_no_changes(self):
        """
        Test that the AuditLogger context manager sets diff to en empty object, and that
        it does not create a log entry.
        """
        product = create_product(name="Awesome product")

        with AuditLogger(instance=product) as audit_logger:
            ...

        assert audit_logger.diff == {}
        assert LogEntry.objects.count() == 0

    def test_auditlogger_context_manager_include_fields(self):
        """
        Test that the AuditLogger context manager only creates log entry with
        applicable fields when include_fields param is passed.
        """
        product = create_product(name="Awesome product")

        with AuditLogger(instance=product, include_fields={"name"}) as audit_logger:
            product.name = "An even more awesome product"
            product.supplier = "A random supplier"

        assert "name" in audit_logger.diff.keys()

        log_entry_changes = LogEntry.objects.first().changes.keys()
        assert "name" in log_entry_changes
        assert "supplier" not in log_entry_changes

    def test_auditlogger_context_manager_exclude_fields(self):
        """
        Test that the AuditLogger context manager only creates log entry with
        applicable fields when exclude_fields param is passed.
        """
        product = create_product(name="Awesome product")

        with AuditLogger(instance=product, exclude_fields={"name"}) as audit_logger:
            product.name = "An even more awesome product"
            product.supplier = "A random supplier"

        assert "name" not in audit_logger.diff.keys()

        log_entry_changes = LogEntry.objects.first().changes.keys()
        assert "supplier" in log_entry_changes

        # Excluded fields
        assert "name" not in log_entry_changes
        assert "created_at" not in log_entry_changes
        assert "updated_at" not in log_entry_changes
