# Django
# Django Rest F.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Models 
from apps.user.models import User

# Serializers 
from apps.user.serializers import UserSerializer, UserLoginSerializer, UserListSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserListSerializer
        elif self.action == 'create':
            return UserSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        ser = UserListSerializer(user)

        res = {
            "user": ser.data,
            "token": token
        }
        return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        data = request.data
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=True)
        user, token = ser.save()
        res = {
            "user": UserListSerializer(user).data,
            "token": token
        }

        return Response(res)