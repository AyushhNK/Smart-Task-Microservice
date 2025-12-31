from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# --------- Register View ---------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            "access": serializer.validated_data['access'],
            "refresh": serializer.validated_data['refresh'],
            "username": serializer.validated_data['user'].username,
            "email": serializer.validated_data['user'].email
        }
        return Response(data, status=status.HTTP_200_OK)

