from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a new Profile
    for a newly registered User.
    """
    if created:
        Profile.objects.create(user=instance, role="reader")


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Signal handler to ensure default groups and their permissions
    exist after migrations are applied.
    """
    # Only run for your app (archive)
    if sender.name != "archive":
        return

    # Example groups (customize names as needed)
    groups_permissions = {
        "Editors": [
            "add_article",
            "change_article",
            "delete_article",
            "view_article",
        ],
        "Publishers": [
            "add_newsletter",
            "change_newsletter",
            "view_newsletter",
        ],
        "Readers": [
            "view_article",
            "view_newsletter",
        ],
    }

    for group_name, perm_codenames in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)

        # Fetch permissions by codename
        perms = Permission.objects.filter(codename__in=perm_codenames)
        group.permissions.set(perms)  # overwrites with the desired set
