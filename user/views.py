from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, SignupSerializer


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


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,  # 요청 데이터 스키마
        responses={200: {"message": "Logged in successfully"}},
        description="로그인 API.",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)  # 세션 생성
            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
