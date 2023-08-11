from rest_framework import generics
from rest_framework import mixins

from .models import Exam, ExamPlan, ExamFavorite
from .serializers import ExamTotalSerializer, ExamDetailSerializer

from rest_framework.views import APIView
from rest_framework import response, status
import xml.etree.ElementTree as ET
import requests
'''
class ExamTotalAPIMixins(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamTotalSerializer
    # GET 메소드 처리 (전체목록)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class ExamDetailAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = ExamPlan.objects.all()
    serializer_class = ExamDetailSerializer
    lookup_field = 'exam_id'
    
    # GET 메소드 처리 (시험ID에 해당하는 1개의 시험 일정 불러옴)
    def get(self, request,*args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    '''
# 시험 정보 DB에 넣는 class
class setExamDB(APIView):
    decodedKey = "YOUR_DECODED_SERVICE_KEY"  # 발급받아야 함
    endPoint = "YOUR_API_ENDPOINT_URL"  # 요청 URL

    def get(self, request, *args, **kwargs):

        def callAPI():
            params = {"serviceKey": self.decodedKey}
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            
            dict = {}
            for item in root.findall('.//item'):
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
            
            return dict
        
        request_data = request.data
        # 필요한 데이터를 직렬화해서 데이터베이스에 저장하는 등의 처리를 여기서 진행
        Exam = callAPI()
        Exam["exam_id"] = request_data["exam_id"]

        serializer = ExamTotalSerializer(data=Exam)
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # /exam/favorite/
# class ExamFavorite(APIView):
#     decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

#     # 시험정보를 조회하는 API의 엔트포인트 주소
#     endPoint = "http://openapi.q-net.or.kr/api/service/rest/InquiryListNationalQualifcationSVC/getList"

#     def get(self,request, *args, **kwargs):
#         # 로그인된 사용자의 user_id 가져오기
#         user_id = request.user_id
#         # def callAPI(user):
#         #     params = {"serviceKey": self.decodedKey}
#         #     response = requests.get(self.endPoint, params=params)
#         #     root = ET.fromstring(response.content)
#         #     dict = {}
#         #     for item in root.findall('.//item'):
#         #         dict["jmcd"] = item.find('jmcd').text #종목코드
#         #         dict["jmfldnm"] = item.find('jmfldnm').text #종목명
#         #         dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
#         #         dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
#         #         dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
#         #         dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
#         #         dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
#         #         dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
#         #         dict["seriescd"]= item.find('seriescd').text #계열코드
#         #         dict["seriesnm"] = item.find('seriesnm').text #계열명
#         def callAPI(user_id):
#             # 이 지점부터 조건문 사용해서 user_id가 있으면 즉, 로그인 되었으면 처리를 해줘야할 것 같기도..?
#             params = {"serviceKey": self.decodedKey} # API 호출을 위한 파라미터 설정
#             response = requests.get(self.endPoint, params=params) # API 호출 및 응답 받기
#             root = ET.fromstring(response.content) # XML 응답을 파싱해 데이터 추출
#             data_list = []

#             # API 응답에서 시험정보 추출해서 리스트에 저장
#             for item in root.findall('.//item'):
#                 data = {
#                     "jmcd": item.find('jmcd').text,
#                     "jmfldnm": item.find('jmfldnm').text,
#                     "mdobligfldnm": item.find('mdobligfldnm').text,
#                     "obligfldnm": item.find('obligfldnm').text,
#                     "qualgbcd": item.find('qualgbcd').text,
#                     "qualgbnm": item.find('qualgbnm').text,
#                     "seriesnm": item.find('seriesnm').text,
#                 }
#                 data["user_id"] = user_id  # user_id 추가
#                 data_list.append(data)

#             return data_list  
        
        
#         request_data = request.data # 요청 데이터를 가져옴
#         exam_favorite = callAPI(request_data["user_id"])    # 사용자가 즐찾한 시험정보 호출..?

#         serializer = ExamTotalSerializer(data = exam_favorite)
#         if serializer.is_valid():
#             serializer.save() # 데이터베이스에 저장
#             return response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # 시리얼라이저가 유효하지 않으면 에러 응답 반환
#         return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /exam/ 시험 전체 목록을 제공하는 API입니다. => 로그인 시 각 시험의 즐겨찾기 여부도 제공
class ExamInfoView(APIView):
    
    def get(self, request, some_exam_id): # exam_id는 프론트에서 다 넘겨줘야할듯..? -> is_favorite을 채우려면
        exam = Exam.objects.get(pk=some_exam_id)  # 해당 exam_id의 Exam 객체를 가져옴
        user_id = request.data.get('user_id')
        if request.user.is_authenticated:
            # 로그인한 사용자
            # ExamFavorite 클래스에서 user_id와 exam_id를 확인
            is_favorite_exists = ExamFavorite.objects.filter(user=request.user, exam_id=some_exam_id).exists()
            is_favorite = True if is_favorite_exists else False
        else:
            # 로그인하지 않은 사용자
            is_favorite = None

        serializer = ExamTotalSerializer(exam)  # Exam 객체를 시리얼라이징
        exam_data = serializer.data  # 시리얼라이즈된 데이터 가져오기

        return response(exam_data, status=status.HTTP_200_OK)

class ExamDetail(APIView):
    # def get(self, request, *args, **kwargs):
    #     # 예시: URL 파라미터에서 필터링 조건을 받아옴
    #     filter_param = request.GET.get('filter_param')

    #     if filter_param:
    #         queryset = YourModel.objects.filter(some_field=filter_param)
    #     else:
    #         queryset = YourModel.objects.all()

    #     serializer = YourModelSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

    # 시험 일정
    endPoint = "http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList"

    def get(self, request, *args, **kwargs):
        def callAPI(qualgbCd, jmCd):
            qualgbCd = request_data['qualgbCd']
            jmCd = request_data['jmCd']
            params = {"serviceKey": self.decodedKey,
            "implYy": "2023",
            "qualgbCd": qualgbCd, #request
            "jmCd": jmCd, #request
            "numOfRows": "1", #임시
            "pageNo": "1",
            "dataFormat": "xml"
            }
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            dict = {}
            for item in root.findall('.//item'):
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
            
            return dict

        request_data = request.data
        # additional_info = request.META.get('HTTP_X_ADDITIONAL_INFO', None)  # 예시로 요청 헤더에서 추가 정보를 가져옴
        examPlan = callAPI(request_data["qualgbCd"], request_data["jmCd"])
        examPlan["exam_id"] = request_data["exam_id"]

        serializer = ExamDetailSerializer(data=examPlan)
        
        if serializer.is_valid():
            serializer.save()  # 데이터베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
