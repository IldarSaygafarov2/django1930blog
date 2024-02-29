from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView

from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from .models import Article, Category, Comment, ArticleCountViews, Like, Dislike


class HomePageView(ListView):
    model = Article
    template_name = 'blog_app/index.html'
    context_object_name = 'articles'


class SearchResults(HomePageView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        # title__icontains=query
        # title__iregex=query
        return Article.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = '/'


def user_logout(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'blog_app/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)


def home_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)


def get_category_articles_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)

# [1,1,1,1,1,1,1,1,1,1]
# [[1,1], [1,1]]


def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = Comment.objects.filter(article=article)

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)


    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()  # http://127.0.0.1:8000/articles/1

            try:
                form.likes
            except Exception as e:
                Like.objects.create(comment=form)

            try:
                form.dislikes
            except Exception as e:
                Dislike.objects.create(comment=form)

            return redirect('detail', article.pk)

    else:
        form = CommentForm()

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    viewed_articles = ArticleCountViews.objects.filter(article=article, session_id=session_id)

    if viewed_articles.count() == 0 and session_id != 'None':
        viewed = ArticleCountViews()
        viewed.article = article
        viewed.session_id = session_id
        viewed.save()

        article.views += 1
        article.save()

    likes = article.likes.user.all().count()
    dislikes = article.dislikes.user.all().count()
    comment_likes = {comment.pk: comment.likes.user.all().count() for comment in comments}
    comment_dislikes = {comment.pk: comment.dislikes.user.all().count() for comment in comments}
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'dislikes': dislikes,
        'likes': likes,
        'comment_likes': comment_likes,
        'comment_dislikes': comment_dislikes
    }
    return render(request, 'blog_app/detail.html', context)


@login_required(login_url='login')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('detail', form.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'blog_app/article_form.html', context)


def author_view(request, user_pk):
    user = User.objects.get(pk=user_pk)
    articles = Article.objects.filter(author=user)
    context = {
        'user': user,
        'articles': articles
    }
    return render(request, 'blog_app/author_page.html', context)


def add_vote(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404

    obj = None

    if obj_type == 'article':
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == 'comment':
        obj = get_object_or_404(Comment, pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)

    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if action == 'add_like':
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)

    return redirect(request.environ['HTTP_REFERER'])