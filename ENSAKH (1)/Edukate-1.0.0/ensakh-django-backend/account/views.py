from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .serializers import LoginSerializer, UserSerializer, ProfessorProfileSerializer, StudentProfileSerializer
from .models import User

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Get profile data based on user type
            profile_data = {}
            if user.user_type == 'teacher':
                profile = user.professor_profile
                profile_data = ProfessorProfileSerializer(profile).data
            elif user.user_type == 'student':
                profile = user.student_profile
                profile_data = StudentProfileSerializer(profile).data
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'profile': profile_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user