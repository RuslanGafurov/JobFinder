from django.urls import path

from users.views import login_view, logout_view, registration_view, update_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', update_view, name='profile'),
    path('registration/', registration_view, name='registration'),
]
