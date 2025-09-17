from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Newsletter, Publisher, Profile


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializes Profile with set fields.
    '''
    class Meta:
        model = Profile
        fields = ["role", "subscribed_journalists"]
        extra_kwargs = {
            "subscribed_journalists": {"read_only": True}
        }


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializes User with set fields.
    '''
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "profile"]


class JournalistSerializer(serializers.ModelSerializer):
    '''
    Serializes Journalist with set fields.
    '''
    articles = serializers.SerializerMethodField()
    newsletters = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "articles", "newsletters"]

    def get_articles(self, obj):
        # Only return published articles for this journalist
        published_articles = obj.articles.filter(status="published")
        return ArticleSerializer(published_articles, many=True).data

    def get_newsletters(self, obj):
        # Only return published newsletters for this journalist
        published_newsletters = obj.newsletters.filter(status="published")
        return NewsletterSerializer(published_newsletters, many=True).data


class PublisherSerializer(serializers.ModelSerializer):
    '''
    Serializes Publisher with set fields.
    '''
    editors = UserSerializer(many=True, read_only=True)
    journalists = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ["id", "name", "description", "editors", "journalists"]


class ArticleSerializer(serializers.ModelSerializer):
    '''
    Serializes Article with set fields.
    '''
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "content", "author", "status", "published_at"]


class NewsletterSerializer(serializers.ModelSerializer):
    '''
    Serializes the Newsletter with set fields.
    '''
    author = UserSerializer(read_only=True)

    class Meta:
        model = Newsletter
        fields = ["id", "title", "content", "author", "status", "published_at"]
