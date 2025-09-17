from django.contrib import admin
from .models import Article, Newsletter, Publisher

# Register your models here.
admin.site.register(Article)
admin.site.register(Newsletter)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "description")