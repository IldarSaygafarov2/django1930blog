from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Article, ArticleCountViews, Like, Dislike, Comment
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from django.views.generic import UpdateView, DeleteView, ListView
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.


# request - Обязательный аргумент каждой функции внутри файла views.py
# http://127.0.0.1:8000/

"""
select * from web_site_category
"""


class HomePageView(ListView):
    model = Article
    template_name = 'web_site/index.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        page = self.request.GET.get('page')
        paginator = context['paginator']
        articles = paginator.get_page(page)
        context['articles'] = articles
        return context


class SearchResults(HomePageView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        # title__icontains - полное сходство значения для проверки
        # title__iregex -
        return Article.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'web_site/article_form.html'
    # success_url = '/'


class DeleteArticle(DeleteView):
    model = Article
    template_name = 'web_site/article_confirm_delete.html'
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
    return render(request, 'web_site/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        # request.POST
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'web_site/registration.html', context)


def home_view(request):
    # categories = Category.objects.all()
    articles = Article.objects.all()

    context = {
        # "categories": categories,
        "articles": articles
    }
    return render(request, 'web_site/index.html', context)


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'articles': articles
    }
    return render(request, 'web_site/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comments = article.comments.all()

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
            form.save()

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

    session_key = request.session.session_key
    viewed_articles = ArticleCountViews.objects.filter(article=article, session_id=session_key)
    if viewed_articles.count() == 0 and session_key != 'None':
        item = ArticleCountViews()
        item.article = article
        item.session_id = session_key
        item.save()

        article.views += 1
        article.save()

    likes = article.likes.user.all().count()
    dislikes = article.dislikes.user.all().count()
    comment_likes = {comment.pk: comment.likes.user.all().count() for comment in comments}
    comment_dislikes = {comment.pk: comment.dislikes.user.all().count() for comment in comments}

    liked_user = article.likes.user.filter(pk=request.user.pk).first()
    disliked_user = article.dislikes.user.filter(pk=request.user.pk).first()

    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes,
        'liked_user': liked_user,
        'disliked_user': disliked_user,
        'comment_likes': comment_likes,
        'comment_dislikes': comment_dislikes
    }
    return render(request, 'web_site/detail.html', context)


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
    return render(request, 'web_site/article_form.html', context)


def author_page(request, user_id):
    user = User.objects.get(pk=user_id)
    articles = Article.objects.filter(author=user)
    comments = [article.comments.all().count() for article in articles]
    views = [article.views for article in articles]
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])

    context = {
        'user': user,
        'articles': articles,
        'total_comments': sum(comments),
        'views': sum(views),
        'total_likes': total_likes,
        'total_dislikes': total_dislikes
    }
    return render(request, 'web_site/author_page.html', context)


# obj_type = article, comment

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
