import uuid
import json
from accounts.models import User, UserManager
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from testmate.settings import KAKAO_REDIRECT_URI
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from rest_framework import permissions


from rest_framework_simplejwt.tokens import RefreshToken

# 필요한 모듈 및 클래스를 가져옵니다
BASE_URL = 'http://localhost:8000/'  # 애플리케이션의 기본 URL을 정의합니다
KAKAO_CALLBACK_URI = KAKAO_REDIRECT_URI
@permission_classes ([permissions.AllowAny])
@api_view(['POST'])
def kakao_callback(request):
    """
    프론트엔드에서 액세스 토큰을 가져옵니다
    """
    # 'Bearer: ' 접두어를 제거하여 클라이언트로부터 받은 액세스 토큰을 추출합니다.
    access_token = json.loads(request.body)['Authorization']
    """
    카카오 API로 사용자의 이메일 정보를 요청
    """
    email_req = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": access_token})
    email_req_status = email_req.status_code
    # 이메일 정보를 성공적으로 받아왔는지 확인
    if email_req_status != 200:
        return JsonResponse({'err_msg': '이메일을 가져오는데 실패했습니다'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email') # 이메일

    # 사용자 정보를 가공
    kakao_account = email_req_json.get('kakao_account', {})  # 기본값으로 빈 딕셔너리 사용
    profile = kakao_account.get('profile', {})

    kakao_id = email_req_json.get('id')  # 카카오 아이디
    email = kakao_account.get('email')  # 이메일
    profile_nickname = profile.get('nickname')  # 닉네임
    profile_image = profile.get('thumbnail_image_url')  # 프로필 사진


    """
    가입 또는 로그인 요청
    """
    try:
        # 1. 유저 모델, 유저 매니저에서 유저 정보 가져오는 함수 (get(email=email))
        user = User.objects.get(email = email)
        if user is None: raise
        # 2. 해당 정보로 access token, refresh token 발급
        refresh = RefreshToken.for_user(user)

        # 3. return Response()
        
        # Add the 'accessToken' field to the user_info dictionary
        

        # Serialize the user info using the extended serializer
        serializer = UserInfoSerializer(instance=user)
        response_body = serializer.data
        response_body['user_id'] = response_body.pop('pk')
        response_body['accessToken'] = str(refresh.access_token) # Replace with the actual access token
        return Response({'information':response_body}, status= status.HTTP_201_CREATED)

    except:
        # 1. 유저 모델, 유저 매니저에서 유저 정보 생성하는 함수 ( create_user(email= "", ... etc))
        extra_fields = {
        'kakao_id': kakao_id,
        'profile_nickname': profile_nickname,
        'profile_image': profile_image,
        }
        user = User.objects.create_user(email=email, password='', **extra_fields)

        # 2. 해당 정보로 access token, refresh token 발급
        refresh = RefreshToken. for_user(user)

        # 3. return Response()
        # Serialize the user info using the extended serializer
        serializer = UserInfoSerializer(user)
        response_body = serializer.data
        response_body['user_id'] = response_body.pop('pk')
        response_body['accessToken'] = str(refresh.access_token) # Replace with the actual access token
        return Response({'information':response_body}, status= status.HTTP_201_CREATED)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
