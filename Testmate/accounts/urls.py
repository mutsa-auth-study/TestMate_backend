from .views import kakao_callback
from django.urls import path

urlpatterns = [
# path('accounts/login/kakao/', kakao_login, name='kakao_login'),
path('accounts/login/kakao/callback/', kakao_callback, name = 'kakao_callback'),
]