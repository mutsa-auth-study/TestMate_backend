# views.py
from django.shortcuts import redirect 
import urllib 
import requests

# code 요청
def kakao_login(request):
    app_rest_api_key = '49e1a5c3a4e15f6c7cf6c68f71615682'
    redirect_uri = 'http://127.0.0.1:8000/accounts/login/kakao/callback/'
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )
    
    
# access token 요청
# def kakao_callback(request):                                                                  
#     params = urllib.parse.urlencode(request.GET)                                      
#     return redirect(f'http://127.0.0.1:8000/accounts/login/kakao/callback/?{params}')

def kakao_callback(request):
    code = request.GET.get("code")

    # Access Token 요청
    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": "49e1a5c3a4e15f6c7cf6c68f71615682", # Rest API 키
            "redirect_uri": "http://127.0.0.1:8000/accounts/login/kakao/callback/",
            "code": code,
        },
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")

    # 사용자 정보 요청
    user_info_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_info_json = user_info_request.json()

    # 이후 사용자 정보를 사용하여 로그인 처리 등의 로직 수행
    # ...

    return redirect('/') # 메인 페이지나 원하는 페이지로 리다이렉션