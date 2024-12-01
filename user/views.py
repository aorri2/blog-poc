from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer


class SignupView(APIView):
    @extend_schema(
        request=SignupSerializer,  # 요청 데이터 스키마
        responses={201: {"message": "User created successfully"}},
        description="회원가입 API. 새로운 사용자를 생성하고 세션을 생성합니다.",
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
