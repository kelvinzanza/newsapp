from django.db import models
from django.contrib.auth.models import User

# Choices for the content's publication status
STATUS_CHOICES = [
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('published', 'Published'),
]

# Choices for user roles.
ROLE_CHOICES = (
    ('reader', 'Reader'),
    ('editor', 'Editor'),
    ('journalist', 'Journalist'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles"
    )

    # subscribing to journalists
    subscribed_journalists = models.ManyToManyField(
        User, blank=True, related_name="followers"
    )

    # subscribing to publishers
    subscribed_publishers = models.ManyToManyField(
        'Publisher', blank=True, related_name="followers"
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        User, related_name="publisher_editors", blank=True
    )
    journalists = models.ManyToManyField(
        User, related_name="publisher_journalists", blank=True
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='articles')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # approval fields
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="approved_articles",
        on_delete=models.SET_NULL
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='newsletters')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # approval fields
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="approved_newsletters",
        on_delete=models.SET_NULL
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
