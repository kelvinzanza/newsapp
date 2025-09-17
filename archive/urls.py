from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Editor
    path('editor_dashboard/', views.editor_dashboard,
         name='editor_dashboard'),
    path('approve_article/<int:article_id>/', views.approve_article,
         name='approve_article'),
    path('reject_article/<int:article_id>/', views.reject_article,
         name='reject_article'),
    path('publish_article/<int:article_id>/', views.publish_article,
         name='publish_article'),
    path('approve_newsletter/<int:newsletter_id>/', views.approve_newsletter,
         name='approve_newsletter'),
    path('reject_newsletter/<int:newsletter_id>/', views.reject_newsletter,
         name='reject_newsletter'),
    path('publish_newsletter/<int:newsletter_id>/', views.publish_newsletter,
         name='publish_newsletter'),

    # Publishers
    path('publishers/', views.publishers_list, name='publishers_list'),
    path('publishers/<int:pk>/', views.publisher_detail,
         name='publisher_detail'),

    # Journalists
    path('journalists/', views.journalists_list, name='journalists_list'),
    path('journalists/<str:username>/', views.articles_by_journalist,
         name='articles_by_journalist'),

    # Articles
    path('articles/<int:article_id>/', views.article_detail,
         name='article_detail'),
    path('create_article/', views.create_article, name='create_article'),
    path('edit_article/<int:article_id>/', views.edit_article,
         name='edit_article'),
    path('delete_article/<int:article_id>/', views.delete_article,
         name='delete_article'),

    # Newsletters
    path('newsletters/<int:newsletter_id>/', views.newsletter_detail,
         name='newsletter_detail'),
    path('create_newsletter/', views.create_newsletter,
         name='create_newsletter'),
    path('edit_newsletter/<int:newsletter_id>/', views.edit_newsletter,
         name='edit_newsletter'),
    path('delete_newsletter/<int:newsletter_id>/', views.delete_newsletter,
         name='delete_newsletter'),

    # User Submissions
    path('my_submissions/', views.my_submissions, name='my_submissions'),

    # Subscription URLs
    path('subscribe/publisher/<int:pk>/',
         views.subscribe_to_publisher,
         name='subscribe_to_publisher'),
    path('unsubscribe/publisher/<int:pk>/',
         views.unsubscribe_from_publisher,
         name='unsubscribe_from_publisher'),
    path('subscribe/journalist/<int:pk>/',
         views.subscribe_to_journalist,
         name='subscribe_to_journalist'),
    path('unsubscribe/journalist/<int:pk>/',
         views.unsubscribe_from_journalist,
         name='unsubscribe_from_journalist'),
    path('my-subscriptions/', views.my_subscriptions_view,
         name='my_subscriptions'),
]
