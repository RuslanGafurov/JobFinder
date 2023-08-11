from django.urls import path

from users.views import (contact_view, delete_view, login_view, logout_view,
                         registration_view, update_view)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete/', delete_view, name='delete'),
    path('profile/', update_view, name='profile'),
    path('contact/', contact_view, name='contact'),
    path('registration/', registration_view, name='registration'),
]
