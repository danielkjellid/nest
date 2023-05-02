from datetime import datetime

import pytest

from nest.core.utils import format_date, format_datetime, format_time

DT = datetime(2020, 1, 1, 12, 30, 45)


class TestDatesUtil:
    @pytest.mark.parametrize(
        "kwargs, expected",
        [
            (dict(), "1 Jan"),
            (dict(with_weekday=True), "Wed, 1 Jan"),
            (dict(with_year=True), "1 Jan 2020"),
            (dict(with_weekday=True, with_year=True), "Wed, 1 Jan 2020"),
        ],
    )
    def test_format_date(self, kwargs, expected):
        assert format_date(DT.date(), **kwargs) == expected

    @pytest.mark.parametrize(
        "kwargs, expected",
        [
            (dict(), "12:30"),
            (dict(with_seconds=True), "12:30:45"),
            (dict(with_decis=True), "12:30:45.0"),
            (dict(with_millis=True), "12:30:45.000"),
            (dict(with_seconds=True, with_decis=True), "12:30:45.0"),
        ],
    )
    def test_format_time(self, kwargs, expected):
        assert format_time(DT.time(), **kwargs) == expected

    @pytest.mark.parametrize(
        "with_weekday",
        [
            False,
            True,
        ],
    )
    def test_format_datetime(self, with_weekday):
        expected = f"1 Jan 2020 {DT.strftime('%H:%M')}"

        if with_weekday is True:
            expected = f"{DT.strftime('%a, ')}{expected}"

        dt = format_datetime(DT, with_weekday=with_weekday)

        assert expected == dt
