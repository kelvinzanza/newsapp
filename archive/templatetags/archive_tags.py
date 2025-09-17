from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_reader')
def is_reader(user):
    '''
    Checks if a user belongs to the 'Reader' group.
    '''
    if user.is_authenticated:
        return user.groups.filter(name='Reader').exists()
    return False

@register.filter(name='is_contributor')
def is_contributor(user):
    '''
    Checks if a user belongs to the 'Journalist' group.
    '''
    if user.is_authenticated:
        return user.groups.filter(name='Journalist').exists()
    return False

@register.filter(name='is_editor')
def is_editor(user):
    '''
    Checks if a user belongs to the 'Editor' group.
    '''
    if user.is_authenticated:
        return user.groups.filter(name='Editor').exists()
    return False

@register.filter(name='get_model_name')
def get_model_name(obj):
    '''
    Returns the name of the object's model class.
    '''
    return obj.__class__.__name__
