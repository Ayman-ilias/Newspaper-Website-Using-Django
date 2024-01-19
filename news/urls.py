from django.urls import path,include
from .import views
from .views import DetailPostView

urlpatterns = [
    path('add/',views.add_post, name='add_post'),
    path('edit/<int:id>/',views.edit_post, name='edit_post'),
    path('delte/<int:id>/',views.delete_post, name='delete_post'),
    path('add_category/',views.add_category, name='add_category'),
    # path('detail/<int:id>/',DetailPostView.as_view(), name='detail_news'),
    path('detail/<int:id>/',DetailPostView.as_view(), name='detail_news'),


]
