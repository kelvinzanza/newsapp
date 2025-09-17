from django.contrib.auth.models import Group

def role_context(request):
    '''
    Adds user role information to the template context.
    The variables 'is_editor' and 'is_contributor' are
    made available to all templates.
    '''
    is_editor = False
    is_contributor = False
    
    if request.user.is_authenticated:
        try:
            # Check if the user belongs to the 'Editor' group
            editor_group = Group.objects.get(name='Editor')
            if editor_group in request.user.groups.all():
                is_editor = True
            
            # Check if the user belongs to the 'Journalist' group
            journalist_group = Group.objects.get(name='Journalist')
            if journalist_group in request.user.groups.all():
                is_contributor = True
        except Group.DoesNotExist:
            # Handle cases where the groups don't exist
            pass
            
    return {
        'is_editor': is_editor,
        'is_contributor': is_contributor,
    }
