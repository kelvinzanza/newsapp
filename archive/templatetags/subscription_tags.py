from django import template
from ..models import Profile

register = template.Library()

@register.filter
def is_subscribed_to_publisher(user, publisher):
    """
    Checks if a user is subscribed to a specific publisher.
    """
    if user.is_authenticated:
        # Check if the publisher exists in the user's subscribed_publishers field
        return user.profile.subscribed_publishers.filter(pk=publisher.pk).exists()
    return False

@register.filter
def is_subscribed_to_journalist(user, journalist):
    """
    Checks if a user is subscribed to a specific journalist.
    """
    if user.is_authenticated:
        # Check if the journalist exists in the user's subscribed_journalists field
        return user.profile.subscribed_journalists.filter(pk=journalist.pk).exists()
    return False