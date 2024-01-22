from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug= models.SlugField(max_length=100,null=True, blank= True,unique = True)


    def __str__(self):
        return self.name


    

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ManyToManyField(Category) 
    writter = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='uploads/', blank = True, null = True) 

    date = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(News, on_delete=models.CASCADE ,related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" comments by {self.user}"
    