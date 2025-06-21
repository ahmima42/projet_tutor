from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Professor, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'avatar']
        read_only_fields = ['id']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError("Identifiant ou mot de passe incorrect.")
            
            if user.user_type != user_type:
                raise serializers.ValidationError(f"Vous n'êtes pas autorisé à vous connecter en tant que {user_type}.")
            
            data['user'] = user
        else:
            raise serializers.ValidationError("Identifiant et mot de passe sont requis.")
        
        return data

class ProfessorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Professor
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'