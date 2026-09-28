import jdatetime

from django import template


register = template.Library()


@register.filter
def persian_datetime(value):

    if not value:
        return ""

    date = jdatetime.datetime.fromgregorian(datetime=value)

    months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]

    return (
        f"{date.day} "
        f"{months[date.month - 1]} "
        f"{date.year}، "
        f"ساعت {date.hour:02d}:{date.minute:02d}"
    )
