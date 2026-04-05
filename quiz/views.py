from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Quiz, Question, Option, UserAttempt, UserAnswer, Result, OTPRecord
from .serializers import QuizSerializer, UserAttemptSerializer, UserAnswerSerializer, ResultSerializer
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = str(random.randint(100000, 999999))
        OTPRecord.objects.create(email=email, otp_code=otp)
        
        subject = 'Your QuizPortal Verification Code'
        message = f'Your 6-digit verification code is: {otp}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        try:
            send_mail(subject, message, email_from, recipient_list)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        otp_record = OTPRecord.objects.filter(email=email, otp_code=otp, is_verified=False).last()
        
        if otp_record:
            # Check for expiration (e.g., 5 minutes)
            time_diff = timezone.now() - otp_record.created_at
            if time_diff.total_seconds() > 300:
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                
            otp_record.is_verified = True
            otp_record.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# Root API View
@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Quiz Portal API',
        'endpoints': {
            'quizzes': '/api/quizzes/',
            'attempts': '/api/attempts/',
            'answers': '/api/answers/',
            'results': '/api/results/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'refresh': '/api/auth/token/refresh/',
            },
            'forgot_password': '/api/forgot-password/',
        }
    })


# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'otp']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            raise serializers.ValidationError("Email and OTP are required.")

        # Check for latest valid OTP record
        otp_record = OTPRecord.objects.filter(email=email, otp_code=otp, is_verified=False).last()
        
        if not otp_record:
            raise serializers.ValidationError("Invalid or already used verification code.")

        # Check for expiration (5 minutes)
        time_diff = timezone.now() - otp_record.created_at
        if time_diff.total_seconds() > 300:
            raise serializers.ValidationError("Verification code has expired. Please request a new one.")

        # Accept the OTP (mark as verified)
        otp_record.is_verified = True
        otp_record.save()
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# Custom Login View (optional, default TokenObtainPairView works too)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout View (Blacklist token)
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            return Response({'error': 'Email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Look up user by email instead of username+email combination for better usability
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found with provided email.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class UserAttemptViewSet(viewsets.ModelViewSet):
    queryset = UserAttempt.objects.all()
    serializer_class = UserAttemptSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        attempt.completed_at = timezone.now()
        attempt.save()
        # Basic scoring logic
        correct_answers = 0
        answers = attempt.answers.all()
        for answer in answers:
            if answer.selected_option and answer.selected_option.is_correct:
                correct_answers += 1
        result = Result.objects.create(attempt=attempt, score=correct_answers)
        return Response({'message': 'Quiz submitted successfully', 'score': correct_answers})

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
