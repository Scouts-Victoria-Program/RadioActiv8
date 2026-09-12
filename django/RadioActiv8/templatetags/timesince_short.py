from django import template
from django.utils.timesince import timesince
from django.utils.translation import ngettext_lazy

register = template.Library()
TIME_STRINGS = {
    "year": ngettext_lazy("%(num)dy", "%(num)dy", "num"),
    "month": ngettext_lazy("%(num)dmo", "%(num)dmo", "num"),
    "week": ngettext_lazy("%(num)dw", "%(num)dw", "num"),
    "day": ngettext_lazy("%(num)dd", "%(num)dd", "num"),
    "hour": ngettext_lazy("%(num)dh", "%(num)dh", "num"),
    "minute": ngettext_lazy("%(num)dm", "%(num)dm", "num"),
}


@register.filter("timesince_short", is_safe=False)
def timesince_filter(value, arg=None):
    """Format a date as the time since that date (i.e. "4d, 6h")."""
    if not value:
        return ""
    try:
        if arg:
            return timesince(value, arg)
        return timesince(value, time_strings=TIME_STRINGS)
    except (ValueError, TypeError):
        return ""
