from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from .models import Publisher, Article, Profile, Newsletter


class ArticleAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create user groups
        self.editor_group = Group.objects.create(name='Editor')
        self.journalist_group = Group.objects.create(name='Journalist')

        # Create users
        self.reader = User.objects.create_user(username="reader", password="123")
        self.editor = User.objects.create_user(username="editor", password="123")
        self.journalist = User.objects.create_user(
            username="journalist",
            password="123"
        )
        self.journalist2 = User.objects.create_user(
            username="journalist2",
            password="123"
        )
        
        # Add users to their respective groups
        self.editor_group.user_set.add(self.editor)
        self.journalist_group.user_set.add(self.journalist)
        self.journalist_group.user_set.add(self.journalist2)

        # Create a publisher and link users to it
        self.publisher = Publisher.objects.create(name="Daily Planet")
        self.publisher.editors.add(self.editor)
        self.publisher.journalists.add(self.journalist)
        self.publisher.save()

        # Reader subscribes to the journalist
        self.reader.profile.subscribed_journalists.add(self.journalist)

        # Create an article by the journalist
        self.article = Article.objects.create(
            title="Test Article 1",
            content="Content for article 1",
            author=self.journalist,
            status="published",
        )
        
        # Create a second article by the same journalist, but not published
        self.article2 = Article.objects.create(
            title="Test Article 2",
            content="Content for article 2",
            author=self.journalist,
            status="submitted",
        )
        
        # Create an article by a different journalist
        self.unsubscribed_article = Article.objects.create(
            title="Unsubscribed Article",
            content="Content from another journalist",
            author=self.journalist2,
            status="published",
        )

    def test_reader_sees_subscribed_and_published_articles_only(self):
        '''A reader should only see published articles from journalists
        they follow.
        '''
        self.client.login(username="reader", password="123")
        res = self.client.get("/api/articles/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], "Test Article 1")

    def test_journalist_sees_own_articles(self):
        '''A journalist should be able to see all of their own articles,
        regardless of status.
        '''
        self.client.login(username="journalist", password="123")
        res = self.client.get("/api/articles/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        article_titles = [
            item['title'] for item in res.data
        ]
        self.assertIn("Test Article 1", article_titles)
        self.assertIn("Test Article 2", article_titles)

    def test_editor_sees_all_publishers_articles(self):
        '''An editor should see all articles from journalists linked to their
        publisher.
        '''
        self.client.login(username="editor", password="123")
        res = self.client.get("/api/articles/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        article_titles = [
            item['title'] for item in res.data
        ]
        self.assertIn("Test Article 1", article_titles)
        self.assertIn("Test Article 2", article_titles)
        self.assertNotIn("Unsubscribed Article", article_titles)
        
    def test_unauthenticated_user_sees_only_published_content(self):
        '''An unauthenticated user should only see publicly published
        articles.
        '''
        res = self.client.get("/api/articles/")
        self.assertEqual(res.status_code, 200)
        # Should see two published articles
        self.assertEqual(len(res.data), 2)
        article_titles = [
            item['title'] for item in res.data
        ]
        self.assertIn("Test Article 1", article_titles)
        self.assertIn("Unsubscribed Article", article_titles)
        self.assertNotIn("Test Article 2", article_titles)


class NewsletterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create user groups
        self.editor_group = Group.objects.create(name='Editor')
        self.journalist_group = Group.objects.create(name='Journalist')

        # Create users
        self.reader = User.objects.create_user(
            username="reader2",
            password="123"
        )
        self.journalist = User.objects.create_user(
            username="journalist2",
            password="123"
        )
        
        # Add users to their respective groups
        self.journalist_group.user_set.add(self.journalist)

        # Reader subscribes to journalist
        self.reader.profile.subscribed_journalists.add(self.journalist)

        # Create a newsletter by the journalist
        self.newsletter = Newsletter.objects.create(
            title="Test Newsletter",
            content="Some newsletter content",
            author=self.journalist,
            status="published",
        )

    def test_reader_sees_subscribed_newsletters(self):
        '''A reader should see published newsletters from journalists
        they follow.
        '''
        self.client.login(username="reader2", password="123")
        res = self.client.get("/api/newsletters/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_journalist_sees_own_newsletters(self):
        '''A journalist should be able to see all of their own newsletters.
        '''
        self.client.login(username="journalist2", password="123")
        res = self.client.get("/api/newsletters/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
