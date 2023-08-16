from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('delete/<int:pk>/', delete_view, name='delete'),
    path('contact/', contact_view, name='contact'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
