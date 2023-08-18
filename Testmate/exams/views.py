from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from django.shortcuts import get_list_or_404
import uuid

from locations.pagination import CustomPageNumberPagination
from django.db.models import Count

import xml.etree.ElementTree as ET
import requests
from threading import Lock

lock = Lock()

# 메인 화면 API
class ExamMainView(APIView):
    
    def get(self, request):

        # 비로그인
        if not request.user.is_authenticated:
            # 최근 유저들이 많이 본 시험 3-5 제공
            popular_exams = ExamRecent.objects.values('exam_id').annotate(view_count=Count('exam_id')).order_by('-view_count')
            # top_5_popular_exams = popular_exams[:5]

            examsList = [item['exam_id'] for item in popular_exams[:5]]

        # 로그인
        else:
            user_id =request.user.id
            # 로그인한 사용자가 즐겨찾기한 시험 ID들 가져오기
            examsList= ExamFavorite.objects.filter(user_id=user_id).values_list('exam_id', flat=True)

        # favorite_exam_ids 리스트 내 시험 id를 Exam , ExamPlan 에서 정보 가져오기
        data1 = Exam.objects.filter(exam_id__in=examsList)
        data2 = ExamPlan.objects.filter(exam_id__in=examsList)

        examsList = list(data1.values())
        examsPlanList = list(data2.values())
    
        for i in range(len(examsList)):
            examsList[i].update(examsPlanList[i])

        response_data = {
            "status": status.HTTP_200_OK,
            "information": examsList
        }
        return Response(response_data, status=status.HTTP_200_OK)


# 시험 목록 조회
class ExamListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        data = Exam.objects.all()
        exam_list = list(data.values())  # 시험 정보를 담을 리스트 초기화
        
        if request.user.is_authenticated:
            # 로그인한 사용자일 경우, 즐겨찾기한 시험 ID들을 가져와 리스트로 변환
            data = ExamFavorite.objects.filter(user_id=request.user.id)
            exam_favorites = data.values()
            favorite_exam_ids = [exam_favorite['exam_id_id'] for exam_favorite in exam_favorites]
            print(favorite_exam_ids)
            
            # 즐찾 여부 확인
            for exam in exam_list:
                if exam["exam_id"] in favorite_exam_ids:
                    exam["is_favorite"] = True
                else:
                    exam["is_favorite"] = False
            # 미로그인 사용자는 모두 즐찾X
        else:
            for exam in exam_list:
                exam["is_favorite"] = False

        # 시험들의 리스트 반환
        response_data = {
            "status": status.HTTP_200_OK,
            "information": exam_list
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ExamDetailView(APIView):

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

    # 시험 일정
    endPoint = "http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList"

    def post(self, request, *args, **kwargs):
        examID = kwargs.get('exam_id')
        # 로그인 된 경우 최근 본 시험 데이터 등록
        try :
            if request.user.is_authenticated:
                userID = request.user.id
                
                # 이미 봤으면 패스
                exam = ExamRecent.objects.filter(user_id = userID, exam_id = examID)
                
                if len(exam): raise
                print("새로 조회")
                # 새로운 조회 정보를 저장
                recent_data = {"user_id":userID, "exam_id":examID}
                serializer = ExamRecentSerializer(data=recent_data)
                
                if serializer.is_valid():
                    serializer.save()  # 데이터베이스에 저장
                    print("최근 조회 등록 성공")
                else:
                    print("최근 조회 등록 실패")
                
                # 현재 저장된 조회 정보의 개수 체크
                count = ExamRecent.objects.filter(user_id=userID).count()

                # 10개 초과하는 경우 가장 오래된 정보 삭제
                if count > 10:
                    oldest_exam = ExamRecent.objects.filter(user_id=userID).earliest("recent_id")
                    oldest_exam.delete()
                    print("10개 초과 삭제")
                

            # DB에서 해당 시험 일정 저장된 것 있는지 확인
        except:
            print("이미 조회한 시험")

        # DB에 있으면 꺼내서 호출
        db = ExamPlan.objects.filter(exam_id=examID)
        if len(db):
            print("디비에 저장된 일정")
            response_data = {
                "status": status.HTTP_200_OK,
                "information": list(db.values())
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # DB에 없으면 API 호출
        request_data = request.data
        params = {"serviceKey": self.decodedKey,
            "implYy": "2023",
            "qualgbCd": request_data.get("qualgbCd"), #request
            "jmCd": request_data.get("jmCd"), #request
            "numOfRows": "1", #임시로 1으로 해놓음. 여러개중 하나 어케 고르지..
            "pageNo": "1",
            "dataFormat": "xml"
            }
        response = requests.get(self.endPoint, params=params)
        root = ET.fromstring(response.content)

        # plan = []
        for item in root.findall('.//item'):
            dict = {}

            dict["implYy"] = item.find('implYy').text
            dict["implSeq"] = item.find('implSeq').text
            dict["description"] = item.find('description').text
            dict["docRegStartDt"] = item.find('docRegStartDt').text
            dict["docRegEndDt"] = item.find('docRegEndDt').text
            dict["docExamStartDt"] = item.find('docExamStartDt').text
            dict["docExamEndDt"] = item.find('docExamEndDt').text
            dict["docPassDt"] = item.find('docPassDt').text
            dict["pracRegStartDt"] = item.find('pracRegStartDt').text
            dict["pracRegEndDt"] = item.find('pracRegEndDt').text
            dict["pracExamStartDt"] = item.find('pracExamStartDt').text
            dict["pracExamEndDt"] = item.find('pracExamEndDt').text
            dict["pracPassDt"] = item.find('pracPassDt').text
            
            dict["exam_id"] = examID

            serializer = ExamDetailSerializer(data=dict)
            
            if serializer.is_valid():
                serializer.save()  # 데이터베이스에 저장
                response_data = {
                    "status": status.HTTP_200_OK,
                    "information": [dict]
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_304_NOT_MODIFIED)
            plan.append(dict)
        
        # response_data = {
        #         "status": status.HTTP_200_OK,
        #         "information": plan
        #     }
        # return Response(response_data, status=status.HTTP_200_OK)
            

# 즐겨찾기
class ExamFavoriteView(APIView):
    # 즐겨찾기 조회
    # ExamFavorite 테이블에서 유저 id에 해당하는 시험 id 쭉 가져오고 해당 시험 id에 해당하는 시험정보를 is_favorite 속성을 다 True로 채운 후에 추가해서 응답할

    def get(self, request):
        # 인증
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id

        # 로그인한 사용자가 즐겨찾기한 시험 ID들 가져오기
        favorite_exam_ids = ExamFavorite.objects.filter(user_id=user_id).values_list('exam_id', flat=True)
        # 이미 favorite_exam_ids는 리스트
        # favorite_exam_ids에는 즐찾 시험id가 들어있음

        '''
        exam_list = []
        for id in favorite_exam_ids:
            exam = Exam.objects.get(exam_id = id)
            exam_list.append(exam)
        '''
        # 최적화
        # Exam모델에서 favorite_exam_ids에 있는 exam_id와 일치하는 시험 정보 필드 가져오기
        data = Exam.objects.filter(exam_id__in=favorite_exam_ids)
        exam_list = list(data.values())  # 시험 정보를 담을 리스트 초기화

        # 즐찾 여부 추가
        for exam in exam_list:
            exam["is_favorite"] = True

        # 시험들의 리스트 반환
        response_data = {
            "status": status.HTTP_200_OK,
            "information": exam_list
        }
        return Response(response_data, status=status.HTTP_200_OK)


    # 즐겨찾기 등록
    def post(self, request):
        # POST 하는동안 다른 요청 보류
        with lock:
            # 요청 데이터에서 유저 ID 가져오기
            user_id = request.user.id
            # 요청 데이터에서 즐겨찾기할 시험 ID 가져오기
            exam_id = request.data.get('exam_id')

            # 현재 즐겨찾기한 시험 ID 개수 확인
            favorite_count = ExamFavorite.objects.filter(user_id=user_id).count()
            # 즐겨찾기한 시험 개수가 5개 이상이면 실패 응답 반환
            if favorite_count >= 5:
                return Response({"detail": "You can only add up to 5 exams to favorites."}, status=status.HTTP_400_BAD_REQUEST)

            # 요청 데이터에 exam_id가 없으면 실패 응답 반환
            if not exam_id:
                return Response({"detail": "exam_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

            dict = {"exam_id":exam_id, "user_id":user_id}
            serializer = ExamFavoriteSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()  # 데이터베이스에 저장
                print("즐찾 등록 성공")
                response_data = {
                    "status": status.HTTP_200_OK,
                }
                return Response(response_data, status=status.HTTP_200_OK)
                
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # 즐겨찾기 시험 정보 삭제(delete)
    def delete(self, request):
        # DELETE 하는동안 다른 요청 보류
        with lock:
            user_id = request.user.id
            exam_id = request.data.get('exam_id')

            try:
                # 해당 즐겨찾기 항목 삭제
                favorite = ExamFavorite.objects.get(user_id=user_id, exam_id=exam_id)
                favorite.delete()

                print("즐찾 삭제 성공")
                response_data = {
                    "status": status.HTTP_200_OK,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            # 해당 즐겨찾기 항목이 존재하지 않는 경우
            except ExamFavorite.DoesNotExist:
                return Response({"detail": "Favorite exam not found"}, status=status.HTTP_400_BAD_REQUEST)



# 최근조회 시험 조회 [GET] [exam/recent]
class ExamRecentView(APIView):
    def get(self,request):

    # 인증
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = request.user.id

        # 최근 조회 시험이 없다면 404 반환
        recent_exams_ids = get_list_or_404(ExamRecent.objects.order_by('-recent_id'), user_id=user_id)[:10]
        # recent_exams_ids 리스트 형태
        # recent_exams_ids에는 최근조회 시험id 10개 들어있음

        '''
        # 이건 404 반환 안하는 버전
        recent_exams_ids = ExamRecent.objects.filter(user_id=user_id).order_by('-recent_id')[:10]
        '''
        # 최적화
        # Exam모델에서 favorite_exam_ids에 있는 exam_id와 일치하는 시험 정보 필드 가져오기
        exams = Exam.objects.filter(exam_id__in=recent_exams_ids)

        # 시리얼라이징
        serializer = ExamTotalSerializer(exams, many=True)

        # 반환
        response_data  = {
                    "status" : status.HTTP_200_OK,
                    "information" : serializer.data ,
        }
        return Response(response_data, status=status.HTTP_200_OK)

'''
# 호출은 되지만 xml 읽기에 실패하는듯. 아래에 파일 직접 읽어서 성공함.
class setExamDB(APIView):
    permission_classes = [AllowAny]

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG%2F%2B8nJcLHw%3D%3D"  # 발급받아야 함
    endPoint = "http://openapi.q-net.or.kr/api/service/rest/InquiryListNationalQualifcationSVC/getList"  # 요청 URL

    def post(self, request, *args, **kwargs):
        params = {"serviceKey": self.decodedKey}    # 
        response = requests.get(self.endPoint, params=params)
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            dict = {}
            dict["exam_id"] = uuid.uuid4() #시험id
            dict["jmcd"] = item.find('jmcd').text #종목코드
            dict["jmfldnm"] = item.find('jmfldnm').text #종목명
            dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
            dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
            dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
            dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
            dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
            dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
            dict["seriescd"]= item.find('seriescd').text #계열코드
            dict["seriesnm"] = item.find('seriesnm').text #계열명
            serializer = ExamTotalSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
                print("OK")
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status=status.HTTP_201_CREATED)

# 성공한 클래스
class setExamDB_XML(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        root = ET.parse('examList.xml')
        
        for item in root.findall('.//item'):
            dict = {}
            dict["exam_id"] = uuid.uuid4 #시험id
            dict["jmcd"] = item.find('jmcd').text #종목코드
            dict["jmfldnm"] = item.find('jmfldnm').text #종목명
            dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
            dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
            dict["seriescd"]= item.find('seriescd').text #계열코드
            dict["seriesnm"] = item.find('seriesnm').text #계열명

            dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
            dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
            dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
            dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
            serializer = ExamTotalSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
                print("OK")
            else:
                print("not")
            
            
            
        return Response(status=status.HTTP_201_CREATED)
   

class deleteExamDB_XML(APIView):
    permission_classes = [AllowAny] 

    def delete(self, request, *args, **kwargs):
        root = ET.parse('examList.xml')
        
        for item in root.findall('.//item'):
            data = Exam.objects.filter(jmcd = item.find('jmcd').text)
            for i in data:
                i.delete()
                print("del")
            
        # return Response(status=status.HTTP_201_CREATED)
'''