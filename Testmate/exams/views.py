from rest_framework import generics
from rest_framework import mixins

from .models import Exam, ExamPlan
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

# 시험정보 전체 조회 API
class ExamTotal(APIView):
    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

    # 시험 목록
    endPoint = "http://openapi.q-net.or.kr/api/service/rest/InquiryListNationalQualifcationSVC/getList"

    def get(self,request, *args, **kwargs):
        user_id = request.user_id # 로그인된 사용자의 user_id 가져오기
        # def callAPI(user):
        #     params = {"serviceKey": self.decodedKey}
        #     response = requests.get(self.endPoint, params=params)
        #     root = ET.fromstring(response.content)
        #     dict = {}
        #     for item in root.findall('.//item'):
        #         dict["jmcd"] = item.find('jmcd').text #종목코드
        #         dict["jmfldnm"] = item.find('jmfldnm').text #종목명
        #         dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
        #         dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
        #         dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
        #         dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
        #         dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
        #         dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
        #         dict["seriescd"]= item.find('seriescd').text #계열코드
        #         dict["seriesnm"] = item.find('seriesnm').text #계열명
        def callAPI(user_id):
            # 이 지점부터 조건문 사용해서 user_id가 있으면 즉, 로그인 되었으면 처리를 해줘야할 것 같기도..?
            params = {"serviceKey": self.decodedKey}
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            data_list = []
            for item in root.findall('.//item'):
                data = {
                    "jmcd": item.find('jmcd').text,
                    "jmfldnm": item.find('jmfldnm').text,
                    "mdobligfldcd": item.find('mdobligfldcd').text,
                    "mdobligfldnm": item.find('mdobligfldnm').text,
                    "obligfldcd": item.find('obligfldcd').text,
                    "obligfldnm": item.find('obligfldnm').text,
                    "qualgbcd": item.find('qualgbcd').text,
                    "qualgbnm": item.find('qualgbnm').text,
                    "seriescd": item.find('seriescd').text,
                    "seriesnm": item.find('seriesnm').text,
                }
                data["user_id"] = user_id  # 사용자 ID 추가
                data_list.append(data)
            return data_list  
        
        
        request_data = request.data # 요청 데이터를 가져옴
        exam_favorite = callAPI(request_data["user_id"])

        serializer = ExamTotalSerializer(data = exam_favorite)
        if serializer.is_valid():
            serializer.save() # 데이터베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

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
    
