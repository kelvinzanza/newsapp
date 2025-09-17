# archive/migrations/0008_auto_add_approval_and_publisher.py
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0007_profile_subscribed_publishers'),
    ]

    operations = [
        # Add publisher field to Profile
        migrations.AddField(
            model_name='profile',
            name='publisher',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                to='archive.publisher',
                null=True,
                blank=True,
                related_name='profiles'
            ),
        ),

        # Add approved_by and approved_at to Article
        migrations.AddField(
            model_name='article',
            name='approved_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                null=True,
                blank=True,
                related_name='approved_articles'
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='approved_at',
            field=models.DateTimeField(null=True, blank=True),
        ),

        # Add approved_by and approved_at to Newsletter
        migrations.AddField(
            model_name='newsletter',
            name='approved_by',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                null=True,
                blank=True,
                related_name='approved_newsletters'
            ),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='approved_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
