from django import template
from core.models import Notifications

register = template.Library()


@register.filter
def notifications_item_count(user):
    if user.is_authenticated:
        qs = Notifications.objects.all()
        if qs.exists():
            return qs[0].items.count()
    return 0
