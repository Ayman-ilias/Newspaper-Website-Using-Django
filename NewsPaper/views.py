from django.shortcuts import render
from news.models import News,Category
from django.shortcuts import render, get_object_or_404

# def all_books(request):
#     return render(request,'index.html')


# def home(request, category_slug=None):
#     data = News.objects.all()
#     categories = Category.objects.all()
#     title = "Your Default Title"

#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         data = News.objects.filter(category=category)
#         title = category.name

#     return render(request, 'home.html', {'data': data, 'category': categories, 'title': title})

# from django.shortcuts import render, get_object_or_404

# def category_posts(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     posts = News.objects.filter(category=category)
#     print([post.title for post in data])
#     return render(request, 'category_post.html', {'category': category, 'posts': posts})




def home(request, category_slug=None):
    data = News.objects.all()
    categories = Category.objects.all()
    title = "Home"

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = News.objects.filter(category=category)
        title = category.name

    return render(request, 'home.html', {'data': data, 'category': categories, 'title': title})

from django.db.models import Avg

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    data = News.objects.filter(category=category).annotate(avg_rating=Avg('comments__rating'))
    data = data.order_by('-avg_rating')
    categories = Category.objects.all()
    title = category.name

    return render(request, 'category.html', {'data': data, 'category': categories, 'title': title})