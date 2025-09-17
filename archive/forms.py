from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article, Newsletter, Publisher, Profile


class RegistrationForm(forms.ModelForm):
    '''
    Registration form to use
    '''
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        empty_label="Select your Publisher",
        required=False
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm Password",
                                       widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        role = cleaned_data.get("role")
        publisher = cleaned_data.get("publisher")

        if role in ['editor', 'journalist'] and not publisher:
            self.add_error('publisher', "Publisher is required for this role.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating Article instances.

    Meta:
        model (Article): The model this form is based on.
        fields (list): The fields to include in the form ('title' and 'content').
    """

    class Meta:
        model = Article
        fields = ['title', 'content']


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and updating Newsletter instances.

    Meta:
        model (Newsletter): The model this form is based on.
        fields (list): The fields to include in the form ('title' and 'content').
    """

    class Meta:
        model = Newsletter
        fields = ['title', 'content']


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
