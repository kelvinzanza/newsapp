from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, NewsletterViewSet, JournalistViewSet, UserSubscriptionsViewSet, PublisherViewSet

'''Urls for the api
'''

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'newsletters', NewsletterViewSet, basename='newsletter')
router.register(r'journalists', JournalistViewSet, basename='journalist')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'subscriptions', UserSubscriptionsViewSet, basename='subscription')

urlpatterns = router.urls
