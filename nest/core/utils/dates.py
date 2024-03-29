from datetime import date, datetime, time


def format_date(
    value: date,
    *,
    with_weekday: bool = False,
    with_year: bool = False,
) -> str:
    """
    Format a date.

    Default format:
        1 Jan

    With weekday:
        Fri, 1 Jan

    With year:
        1 Jan 2020
    """

    spec = "%-d %b"
    if with_weekday:
        spec = f"%a, {spec}"
    if with_year:
        spec = f"{spec} %Y"

    formatted = value.strftime(spec)
    return formatted


def format_time(
    value: datetime | time,
    *,
    with_seconds: bool = False,
    with_decis: bool = False,
    with_millis: bool = False,
) -> str:
    """
    Format a time.

    Default format:
        12:30

    With seconds:
        12:30:45

    With decis:
        12:30:45.0

    With millis:
        12:30:45.123
    """

    spec = "%H:%M"
    if with_seconds or with_decis or with_millis:
        spec = f"{spec}:%S"
    if with_decis or with_millis:
        spec = f"{spec}.%f"

    formatted = value.strftime(spec)

    if with_millis:
        formatted = formatted[:-3]
    elif with_decis:
        formatted = formatted[:-5]

    return formatted


def format_datetime(
    value: datetime,
    *,
    with_year: bool = True,
    with_weekday: bool = False,
    with_seconds: bool = False,
    with_decis: bool = False,
    with_millis: bool = False,
) -> str:
    """
    Format a datetime.


    Default format:
        1 Jan 2020 12:30

    Without year:
        1 Jan 12:30

    With seconds:
        1 Jan 2020 12:30:45

    With decis:
        1 Jan 2020 12:30:45.0

    With millis:
        1 Jan 2020 12:30:45.000

    With timezone:
        1 Jan 2020 12:30 (+02:00)

    With weekday:
        Fri, 1 Jan 2020 12:30

    With seconds, millis, and timezone:
        1 Jan 2020 12:30:45.000 (+02:00)
    """

    formatted_date = format_date(
        value.date(),
        with_year=with_year,
        with_weekday=with_weekday,
    )
    formatted_time = format_time(
        value.time(),
        with_seconds=with_seconds,
        with_decis=with_decis,
        with_millis=with_millis,
    )
    formatted = f"{formatted_date} {formatted_time}"

    return formatted
