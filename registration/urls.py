from django.urls import path,include
from .import views
from django.contrib.auth.views import LogoutView
# from django.conf.urls import url

urlpatterns = [
    path('register/',views.register, name='user_registration'),
    path('user_login/',views.UserLoginView.as_view(), name='user_login'),
    path('user_logout/',views.user_logout, name='user_logout'),
    path('profile/',views.profile, name='profile'),
    path('profile/edit',views.edit_profile, name='edit_profile'),
    path('profile/pass_change',views.pass_change, name='pass_change'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    # path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    # path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
    # path('registration/activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
