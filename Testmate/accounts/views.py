import uuid

from accounts.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError
from testmate.settings import KAKAO_REDIRECT_URI
from .serializers import UserInfoSerializer
from rest_framework.response import Response

# 필요한 모듈 및 클래스를 가져옵니다
BASE_URL = 'http://localhost:8000/'  # 애플리케이션의 기본 URL을 정의합니다
KAKAO_CALLBACK_URI = KAKAO_REDIRECT_URI

def kakao_callback(request):
    """
    프론트엔드에서 액세스 토큰을 가져옵니다
    """
    # 'Bearer: ' 접두어를 제거하여 클라이언트로부터 받은 액세스 토큰을 추출합니다
    access_token = request.headers.get('Authorization')[7:]

    """
    카카오 API로 사용자의 이메일 정보를 요청
    """
    email_req = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
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
    nickname = profile.get('nickname')  # 닉네임
    profile_image = profile.get('thumbnail_image_url')  # 프로필 사진

    # 가공한 사용자 정보를 딕셔너리로 저장
    userinfo = {
        'user_id': uuid.uuid4(),
        'kakao_id': kakao_id,
        'profile_nickname': nickname,
        'profile_image': profile_image,
        'email': email
    }
    print(userinfo)



    """
    가입 또는 로그인 요청
    """
    try:
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        user = User.objects.get(email=email)

        data = {'access_token': access_token}   # 이미 제
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        # 로그인 결과 처리
        if accept_status != 200:
            return JsonResponse({'err_msg': '로그인에 실패했습니다'}, status=accept_status)
        accept_json = accept.json()

    except:
        # 기존에 가입된 유저가 없으면 새로 가입 => jwt 토큰 발급?
    
        data = {'access_token': access_token}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러 
        if accept_status != 200:
            return JsonResponse({'err_msg': '가입에 실패했습니다'}, status=accept_status)
        accept_json = accept.json()

    # 가입 또는 로그인한 유저 정보를 가져옴
    user = User.objects.get(email=email)

    # JSON 응답 생성
    accept_json['user_id'] = user.user_id
    accept_json['profile_nickname'] = user.profile_nickname
    accept_json['profile_image'] = user.profile_image.url if user.profile_image.url else None
    accept_json['email'] = user.email
    accept_json['accessToken'] = user.accessToken

    accept_json.pop('user', None)

    response_data = {
        "status": status.HTTP_200_OK,
        "information": [accept_json]
        }

    return JsonResponse(response_data)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
