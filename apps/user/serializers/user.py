# Django
from django.contrib.auth import authenticate, password_validation

# Django Rest F.
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from apps.user.models import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 5, max_length = 15)
    password_confirm = serializers.CharField(min_length = 5, max_length = 15)

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "first_name":{"required":True, "allow_null":False, "allow_blank":False},
            "last_name":{"required":True, "allow_null":False, "allow_blank":False},
            "age":{"required":True, "allow_null":False},
        }

    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password:
            if password != password_confirm:
                raise serializers.ValidationError({"validation":"Las contraseñas no coinciden."})
            password_validation.validate_password(password)
        
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return user, token.key

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username = email, password = password)

        if not user:                
            raise serializers.ValidationError({"error":"El correo electrónico y/o contraseña que ingresó es incorrecto. Verifique sus credenciales"})
        self.context['user'] = user
        
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=user)

        return user, token.key 