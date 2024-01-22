from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RATING_CHOICES
from .forms import PostForm,CommentForm,CategoryForm
from .models import News
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User


def send_email(user,subject, template):
    message = render_to_string(template, {
        'user' : user,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


@login_required
def edit_post(request, id):
    post = News.objects.get(id=id)
    
    if request.user.account.is_editor:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'News updated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid form submission.')
        else:
            form = PostForm(instance=post)
            
        return render(request, 'news.html', {'form': form})
    else:
        messages.warning(request, 'No permission to edit.')
        return redirect('home')

@login_required
def delete_post(request, id):
    post = News.objects.get(id=id)
    
    if request.user.account.is_editor:
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'News deleted successfully.')
            return redirect('home')
        else:
            return render(request, 'delete.html', {'post': post})
    else:
        messages.warning(request, 'No permission to delete.')
        return redirect('home')

# @login_required
# def add_post(request):
#     if request.user.account.is_editor:
#         if request.method == 'POST':
#             form = PostForm(request.POST)
#             if form.is_valid():
#                 form.instance.author = request.user
#                 form.save()
#                 messages.success(request, 'Post added successfully.')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid form submission.')
#         else:
#             form = PostForm()
        
#         return render(request, 'news.html', {'form': form})
#     else:
#         messages.warning(request, 'No permission to add.')
#         return redirect('home')

@login_required
def add_post(request):
    if request.user.account.is_editor:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                messages.success(request, ' added successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid form submission.')
                print(form.errors)
        else:
            form = PostForm()
        
        return render(request, 'news.html', {'form': form})
    else:
        messages.warning(request, 'No permission to add.')
        return redirect('home')


class DetailPostView(DetailView):
    model = News
    template_name = 'detail_news.html'
    context_object_name = 'news'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            news = self.get_object()
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = news
                new_comment.user = request.user
                new_comment.save()
                messages.success(request, 'Thank you for your Rating')
                send_email(request.user, "Review Rating", "ratting_email.html")
            else:
                messages.error(request, 'Invalid Information')
        else:
            messages.error(request, 'You need to be logged in to give a review.')
        
        return redirect('detail_news', id=kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        comments = news.comments.all()
        comment_form = CommentForm()

    
        ratings = [comment.rating for comment in comments]
        if ratings:
            avg_rating = round(sum(ratings) / len(ratings), 2)
        else:
            avg_rating = None

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['stars'] = dict(RATING_CHOICES)
        context['avg_rating'] = avg_rating

        related_articles = News.objects.filter(category__in=news.category.all()).exclude(id=news.id)[:2]
        context['related_articles'] = related_articles

        return context


def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('add_category')
    else:
        category_form = CategoryForm()
    return render(request, 'categories.html', {'form': category_form})