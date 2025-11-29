"""
Unit tests for migration status computation logic.
"""

from src.api.endpoints.health import _compute_migration_status
from src.schemas.health import MigrationStatus


def test_status_up_to_date_when_no_migrations_and_clean_db() -> None:
    assert _compute_migration_status(None, None) is MigrationStatus.UP_TO_DATE


def test_status_pending_when_head_exists_but_db_empty() -> None:
    assert _compute_migration_status("rev1", None) is MigrationStatus.PENDING


def test_status_unknown_when_db_revision_without_head() -> None:
    assert _compute_migration_status(None, "rev1") is MigrationStatus.UNKNOWN


def test_status_up_to_date_when_revisions_match() -> None:
    assert _compute_migration_status("rev1", "rev1") is MigrationStatus.UP_TO_DATE


def test_status_pending_when_revisions_differ() -> None:
    assert _compute_migration_status("rev2", "rev1") is MigrationStatus.PENDING
