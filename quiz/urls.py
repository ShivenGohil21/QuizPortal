from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet, UserAttemptViewSet, UserAnswerViewSet, ResultViewSet,
    RegisterView, CustomTokenObtainPairView, LogoutView, ForgotPasswordView,
    SendOTPView, VerifyOTPView,
    api_root
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'attempts', UserAttemptViewSet)
router.register(r'answers', UserAnswerViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', api_root, name='api_root'),
    path('', include(router.urls)),

    # OTP Authentication APIs
    path('auth/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/register/', RegisterView.as_view(), name='register'),

    # Forgot Password API
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]
