from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Count, Q
from django.http import Http404
from .models import Article, Newsletter, Profile, Publisher
from .forms import RegistrationForm, ArticleForm, NewsletterForm
from itertools import chain
from django.db import transaction


def safe_get_group(name):
    '''
    Helper to safely get or create a group by name.
    '''
    group, _ = Group.objects.get_or_create(name=name)
    return group


def welcome_view(request):
    """
    Render the welcome page with published articles, newsletters, journalists,
    and publishers.

    The view collects published articles and newsletters, combines them into a
    single list ordered by publication date, and fetches all journalists and
    publishers to display on the welcome page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered 'welcome.html' template with context data.
    """
    published_articles = Article.objects.filter(status='published')
    published_newsletters = Newsletter.objects.filter(status='published')

    combined_items = sorted(
        chain(published_articles, published_newsletters),
        key=lambda item: item.published_at,
        reverse=True
    )

    journalist_group = Group.objects.filter(name='Journalist').first()
    journalists = journalist_group.user_set.all() if journalist_group else []

    publishers = Publisher.objects.all()

    context = {
        'items': combined_items,
        'journalists': journalists,
        'publishers': publishers,
    }
    return render(request, 'welcome.html', context)


def is_editor_check(user):
    '''
    Checks if a user is in the 'Editor' group.
    '''
    return user.groups.filter(name='Editor').exists()


def is_contributor_check(user):
    '''
    Checks if a user is in the 'Journalist' or 'Editor' group.
    '''
    return (user.groups.filter(name='Journalist').exists() or
            user.groups.filter(name='Editor').exists())


@login_required
@user_passes_test(is_editor_check)
def editor_dashboard(request):
    '''
    Renders the editor dashboard with submitted and approved articles
    and newsletters.
    '''
    # We use a Q object to filter for articles with a status of 'submitted'
    # OR 'approved'.
    submitted_and_approved_articles = Article.objects.filter(
        Q(status='submitted') | Q(status='approved')
    ).order_by('-created_at')

    submitted_and_approved_newsletters = Newsletter.objects.filter(
        Q(status='submitted') | Q(status='approved')
    ).order_by('-created_at')

    context = {
        'articles': submitted_and_approved_articles,
        'newsletters': submitted_and_approved_newsletters,
    }
    return render(request, 'editor_dashboard.html', context)


@login_required
@user_passes_test(is_editor_check)
def approve_article(request, article_id):
    '''
    Approves a submitted article.
    '''
    if request.method == 'POST':
        article = get_object_or_404(
            Article, id=article_id, status='submitted'
        )
        article.status = 'approved'
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()
        messages.success(request, 'Article approved successfully.')
    return redirect('editor_dashboard')


@login_required
@user_passes_test(is_editor_check)
def reject_article(request, article_id):
    '''
    Rejects a submitted article.
    '''
    if request.method == 'POST':
        article = get_object_or_404(
            Article, id=article_id, status='submitted'
        )
        article.status = 'rejected'
        article.save()
        messages.success(request, 'Article rejected successfully.')
    return redirect('editor_dashboard')


@login_required
@user_passes_test(is_editor_check)
def publish_article(request, article_id):
    '''
    Publishes an approved article.
    '''
    if request.method == 'POST':
        article = get_object_or_404(
            Article, id=article_id, status='approved'
        )
        article.status = 'published'
        article.published_at = timezone.now()
        article.save()
        messages.success(request, 'Article published successfully.')
    return redirect('editor_dashboard')


@login_required
@user_passes_test(is_editor_check)
def approve_newsletter(request, newsletter_id):
    '''
    Approves a submitted newsletter.
    '''
    if request.method == 'POST':
        newsletter = get_object_or_404(
            Newsletter, id=newsletter_id, status='submitted'
        )
        newsletter.status = 'approved'
        newsletter.approved_by = request.user
        newsletter.approved_at = timezone.now()
        newsletter.save()
        messages.success(request, 'Newsletter approved successfully.')
    return redirect('editor_dashboard')


@login_required
@user_passes_test(is_editor_check)
def reject_newsletter(request, newsletter_id):
    '''
    Rejects a submitted newsletter.
    '''
    if request.method == 'POST':
        newsletter = get_object_or_404(
            Newsletter, id=newsletter_id, status='submitted'
        )
        newsletter.status = 'rejected'
        newsletter.save()
        messages.success(request, 'Newsletter rejected successfully.')
    return redirect('editor_dashboard')


@login_required
@user_passes_test(is_editor_check)
def publish_newsletter(request, newsletter_id):
    '''
    Publishes an approved newsletter.
    '''
    if request.method == 'POST':
        newsletter = get_object_or_404(
            Newsletter, id=newsletter_id, status='approved'
        )
        newsletter.status = 'published'
        newsletter.published_at = timezone.now()
        newsletter.save()
        messages.success(request, 'Newsletter published successfully.')
    return redirect('editor_dashboard')


def login_user(request):
    '''
    Handles user login.
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('welcome')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_user(request):
    '''
    Handles user logout.
    '''
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('welcome')


def register(request):
    '''
    Handles user registration and assigns new users to the correct group and
    publisher.
    '''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                password = form.cleaned_data.get("password")
                user.set_password(password)
                user.save()

                # Ensure profile exists
                profile, _ = Profile.objects.get_or_create(user=user)

                # Assign group
                role = form.cleaned_data.get('role')
                publisher = form.cleaned_data.get('publisher')
                group = safe_get_group(role.capitalize())
                user.groups.add(group)

                # Assign publisher if role requires
                if role in ['editor', 'journalist'] and publisher:
                    profile.publisher = publisher
                    profile.save()

                login(request, user)
                messages.success(
                    request, f'Registration successful! You are now a {role}.'
                )
                return redirect('welcome')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def journalists_list(request):
    '''
    Displays a list of all journalists.
    '''
    journalist_group = Group.objects.filter(name='Journalist').first()
    journalists = journalist_group.user_set.all() if journalist_group else []
    if not journalist_group:
        messages.error(request, "The 'Journalist' group does not exist.")

    context = {
        'journalists': journalists
    }
    return render(request, 'journalists_list.html', context)


def publishers_list(request):
    '''
    Displays a list of all publishers (from the Publisher model).
    '''
    publishers = Publisher.objects.all()
    return render(request, 'publishers_list.html', {'publishers': publishers})


def publisher_detail(request, pk):
    '''
    Displays the details of a single publisher.
    '''
    publisher = get_object_or_404(Publisher, pk=pk)
    return render(request, 'publisher_detail.html', {'publisher': publisher})


def articles_by_journalist(request, username):
    '''
    Displays published articles and newsletters by a specific journalist.
    '''
    try:
        author = User.objects.get(username=username)
        articles = Article.objects.filter(
            author=author, status='published'
        ).order_by('-published_at')
        newsletters = Newsletter.objects.filter(
            author=author, status='published'
        ).order_by('-published_at')
        context = {
            'author': author,
            'articles': articles,
            'newsletters': newsletters,
        }
        return render(request, 'articles_by_journalist.html', context)
    except User.DoesNotExist:
        messages.error(request, 'Journalist not found.')
        return redirect('journalists_list')


@login_required
@user_passes_test(is_contributor_check)
def create_article(request):
    '''
    Allows a contributor to create a new article.
    '''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article submitted for approval!')
            return redirect('my_submissions')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})


@login_required
@user_passes_test(is_contributor_check)
def create_newsletter(request):
    '''
    Allows a contributor to create a new newsletter.
    '''
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, 'Newsletter submitted for approval!')
            return redirect('my_submissions')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = NewsletterForm()
    return render(request, 'create_newsletter.html', {'form': form})


@login_required
@user_passes_test(is_contributor_check)
def my_submissions(request):
    '''
    Displays a contributor's submitted articles and newsletters.
    '''
    articles = Article.objects.filter(
        author=request.user
    ).order_by('-created_at')
    newsletters = Newsletter.objects.filter(
        author=request.user
    ).order_by('-created_at')
    context = {
        'articles': articles,
        'newsletters': newsletters,
    }
    return render(request, 'my_submissions.html', context)


@login_required
@user_passes_test(is_contributor_check)
def edit_article(request, article_id):
    '''
    Allows a contributor to edit their own article if it hasn't been
    approved yet.
    '''
    article = get_object_or_404(
        Article, id=article_id, author=request.user
    )
    if article.status != 'submitted':
        messages.error(
            request, "You can only edit articles that are still submitted."
        )
        return redirect('my_submissions')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article.status = 'submitted'
            form.save()
            messages.success(
                request, 'Article updated and resubmitted for approval.'
            )
            return redirect('my_submissions')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})


@login_required
@user_passes_test(is_contributor_check)
def delete_article(request, article_id):
    '''
    Allows a contributor to delete their own article if it hasn't been
    approved yet.
    '''
    article = get_object_or_404(
        Article, id=article_id, author=request.user
    )
    if article.status != 'submitted':
        messages.error(
            request, "You can only delete articles that are still submitted."
        )
        return redirect('my_submissions')

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully.')
    return redirect('my_submissions')


@login_required
@user_passes_test(is_contributor_check)
def edit_newsletter(request, newsletter_id):
    '''
    Allows a contributor to edit their own newsletter if it hasn't been
    approved yet.
    '''
    newsletter = get_object_or_404(
        Newsletter, id=newsletter_id, author=request.user
    )
    if newsletter.status != 'submitted':
        messages.error(
            request,
            "You can only edit newsletters that are still submitted."
        )
        return redirect('my_submissions')

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter.status = 'submitted'
            form.save()
            messages.success(
                request,
                'Newsletter updated and resubmitted for approval.'
            )
            return redirect('my_submissions')
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'edit_newsletter.html', {'form': form})


@login_required
@user_passes_test(is_contributor_check)
def delete_newsletter(request, newsletter_id):
    '''
    Allows a contributor to delete their own newsletter if it hasn't been
    approved yet.
    '''
    newsletter = get_object_or_404(
        Newsletter, id=newsletter_id, author=request.user
    )
    if newsletter.status != 'submitted':
        messages.error(
            request,
            "You can only delete newsletters that are still submitted."
        )
        return redirect('my_submissions')

    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter deleted successfully.')
    return redirect('my_submissions')


@login_required
def article_detail(request, article_id):
    '''
    Displays the content of a single article. Editors can view
    submitted/approved articles, while other users can only view published
    ones.
    '''
    article = get_object_or_404(Article, id=article_id)
    is_author = (request.user == article.author)
    is_editor = is_editor_check(request.user)
    
    if is_author or is_editor:
        return render(request, 'article_detail.html', {'article': article})

    if article.status == 'published':
        return render(request, 'article_detail.html', {'article': article})

    raise Http404("No Article matches the given query.")


def newsletter_detail(request, newsletter_id):
    '''
    Displays the content of a single published newsletter.
    '''
    newsletter = get_object_or_404(
        Newsletter, id=newsletter_id, status='published'
    )
    return render(request, 'newsletter_detail.html',
                  {'newsletter': newsletter})


@login_required
@require_POST
def subscribe_to_publisher(request, pk):
    '''
    Allows a logged-in user to subscribe to a publisher.
    '''
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.profile.subscribed_publishers.add(publisher)
    return redirect('publisher_detail', pk=pk)


@login_required
@require_POST
def unsubscribe_from_publisher(request, pk):
    '''
    Allows a logged-in user to unsubscribe from a publisher.
    '''
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.profile.subscribed_publishers.remove(publisher)
    return redirect('publisher_detail', pk=pk)


@login_required
@require_POST
def subscribe_to_journalist(request, pk):
    '''
    Allows a logged-in user to subscribe to a journalist.
    '''
    journalist = get_object_or_404(User, pk=pk)
    request.user.profile.subscribed_journalists.add(journalist)
    return redirect(
        'articles_by_journalist', username=journalist.username
    )


@login_required
@require_POST
def unsubscribe_from_journalist(request, pk):
    '''
    Allows a logged-in user to unsubscribe from a journalist.
    '''
    journalist = get_object_or_404(User, pk=pk)
    request.user.profile.subscribed_journalists.remove(journalist)
    return redirect(
        'articles_by_journalist', username=journalist.username
    )


@login_required
def my_subscriptions_view(request):
    '''
    Displays a list of all publishers and journalists the user is 
    subscribed to.
    '''
    profile, _ = Profile.objects.get_or_create(user=request.user)
    subscribed_publishers = profile.subscribed_publishers.all()
    subscribed_journalists = profile.subscribed_journalists.all()

    context = {
        'subscribed_publishers': subscribed_publishers,
        'subscribed_journalists': subscribed_journalists
    }
    return render(request, 'my_subscriptions.html', context)
