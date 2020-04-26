from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Votes

register = template.Library()

@register.simple_tag
def get_up_number(content_type_id, object_id):
    try:
        count = Votes.objects.filter(content_type=content_type_id, object_id=object_id, vote_type=True).count()
        return count
    except ContentType.DoesNotExist:
        return 'Unknown'

@register.simple_tag
def get_down_number(content_type_id, object_id):
    try:
        count = Votes.objects.filter(content_type=content_type_id, object_id=object_id, vote_type=False).count()
        return count
    except ContentType.DoesNotExist:
        return 'Unknown'