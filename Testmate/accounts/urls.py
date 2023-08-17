from .import views
from django.urls import path

urlpatterns = [
path('auth/login', views.kakao_callback, name='kakao_callback'),
path('kakao/login/finish/', views.KakaoLogin.as_view(), name = 'kakao_login_todjango'),

path('auth/delete', views.DeleteUser.as_view(), name = 'deleteUser'),
]
