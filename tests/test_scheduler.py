from datetime import datetime, UTC, timedelta
from src.core.checker import is_monitor_due
import pytest


class DummyMonitor:
    def __init__(self, is_active, last_checked_at, check_interval):
        self.is_active = is_active
        self.last_checked_at = last_checked_at
        self.check_interval = check_interval


NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)


class TestMonitorScheduler:

    def test_monitor_never_checked_is_due(self):
        monitor = DummyMonitor(is_active=True, last_checked_at=None, check_interval=30)
        assert is_monitor_due(monitor, NOW) is True

    def test_monitor_inactive(self):
        monitor = DummyMonitor(is_active=False, last_checked_at=None, check_interval=30)
        assert is_monitor_due(monitor, NOW) is False

    def test_monitor_not_yet_due(self):

        monitor = DummyMonitor(
            is_active=True,
            last_checked_at=NOW - timedelta(seconds=10),
            check_interval=30,
        )
        assert is_monitor_due(monitor, NOW) is False

    def test_monitor_due(self):

        monitor = DummyMonitor(
            is_active=True,
            last_checked_at=NOW - timedelta(seconds=30),
            check_interval=30,
        )
        assert is_monitor_due(monitor, NOW) is True

    def test_monitor_overdue(self):
        monitor = DummyMonitor(
            is_active=True,
            last_checked_at=NOW - timedelta(seconds=60),
            check_interval=30,
        )
        assert is_monitor_due(monitor, NOW) is True
