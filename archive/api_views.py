from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import ArticleSerializer, NewsletterSerializer, UserSerializer, JournalistSerializer, PublisherSerializer
from .models import Article, Newsletter, Publisher, Profile
from .permissions import IsContentOwnerOrEditor

# Helper functions to check user groups
def is_journalist(user):
    '''
    Checks if a user belongs to the 'Journalist' group.
    '''
    return user.groups.filter(name='Journalist').exists()

def is_editor(user):
    '''
    Checks if a user belongs to the 'Editor' group.
    '''
    return user.groups.filter(name='Editor').exists()

class ContentQuerysetMixin:
    '''
    A mixin to handle shared queryset logic for Article and Newsletter viewsets.
    This prevents code duplication.
    '''
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset

        if is_editor(user):
            '''
            Editors can see all content from journalists that belong to their publisher.
            '''
            publisher = Publisher.objects.filter(editors=user).first()
            if publisher:
                publisher_journalists = publisher.journalists.all()
                return self.queryset.filter(author__in=publisher_journalists)
            return self.queryset.none()

        if is_journalist(user):
            '''
            Journalists can only see their own content.
            '''
            return self.queryset.filter(author=user)

        if user.is_authenticated:
            '''
            Readers can see published content only from journalists they follow.
            '''
            profile, _ = Profile.objects.get_or_create(user=user)
            subscribed_journalists = profile.subscribed_journalists.all()
            return self.queryset.filter(
                Q(author__in=subscribed_journalists) & Q(status='published')
            )

        '''
        Unauthenticated users can only see publicly published content.
        '''
        return self.queryset.filter(status='published')


class ArticleViewSet(ContentQuerysetMixin, viewsets.ModelViewSet):
    '''
    A ViewSet for articles that handles role-based access to the content.
    '''
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsContentOwnerOrEditor]


class NewsletterViewSet(ContentQuerysetMixin, viewsets.ModelViewSet):
    '''
    A ViewSet for newsletters that handles role-based access to the content.
    '''
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    permission_classes = [IsContentOwnerOrEditor]


class JournalistViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows journalists to be viewed.
    '''
    queryset = User.objects.filter(groups__name='Journalist')
    serializer_class = JournalistSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        '''
        Allows a logged-in user to subscribe to a journalist.
        '''
        journalist = get_object_or_404(User, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.subscribed_journalists.add(journalist)
        return Response({'status': 'subscribed'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        '''
        Allows a logged-in user to unsubscribe from a journalist.
        '''
        journalist = get_object_or_404(User, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.subscribed_journalists.remove(journalist)
        return Response({'status': 'unsubscribed'})


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows publishers to be viewed.
    '''
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class UserSubscriptionsViewSet(viewsets.ViewSet):
    '''
    A viewset for authenticated users to see their subscriptions.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        '''
        Returns a list of all journalists the current user is subscribed to.
        '''
        profile, _ = Profile.objects.get_or_create(user=request.user)
        subscribed_journalists = profile.subscribed_journalists.all()
        serializer = JournalistSerializer(subscribed_journalists, many=True)
        return Response(serializer.data)
