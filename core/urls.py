from django.urls import path
from .views import totp_login_view, setup_totp_view, home_view

urlpatterns = [
    path('login/', totp_login_view, name='login'),
    path('setup-totp/', setup_totp_view, name='setup_totp'),
    path('', home_view, name='home'),
]
