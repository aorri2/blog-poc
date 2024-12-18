from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class SignupViewTest(APITestCase):

    def setUp(self):
        # 테스트 초기화 작업 (필요 시)
        self.signup_url = reverse("user:user_signup")  # 회원가입 API URL

    def test_signup_success(self):
        """회원가입 성공 테스트"""
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.signup_url, payload)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully")

        # 데이터베이스 확인
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_signup_missing_field(self):
        """필드 누락으로 인한 실패 테스트"""
        payload = {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post(self.signup_url, payload)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # email 필드 누락 확인

    def test_signup_duplicate_username(self):
        """중복된 사용자명으로 인한 실패 테스트"""
        # 기존 사용자 생성
        User.objects.create_user(username="testuser", password="password123")

        payload = {
            "username": "testuser",
            "email": "duplicate@example.com",
            "password": "password123",
        }
        response = self.client.post(self.signup_url, payload)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)  # username 중복 에러 확인


class LoginViewTest(APITestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.login_url = "/api/user/login/"

    def test_login_success(self):
        """로그인 성공 테스트"""
        payload = {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post(self.login_url, payload)

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged in successfully")

        # 세션 확인
        self.assertIn("sessionid", response.cookies)

    def test_login_invalid_password(self):
        """잘못된 비밀번호로 인한 로그인 실패 테스트"""
        payload = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, payload)

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_login_missing_fields(self):
        """필드 누락으로 인한 로그인 실패 테스트"""
        payload = {"username": "testuser"}
        response = self.client.post(self.login_url, payload)

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_login_non_existent_user(self):
        """존재하지 않는 유저로 인한 로그인 실패 테스트"""
        payload = {
            "username": "nonexistentuser",
            "password": "password123",
        }
        response = self.client.post(self.login_url, payload)

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
