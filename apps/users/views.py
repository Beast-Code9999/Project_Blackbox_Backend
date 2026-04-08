from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(APIView):
    """
    POST /api/users/register/
    email, password, name
    return user data + JWT 
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            # return validation error so frontend knows what's wrong
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # Generate JWT token pair for the newly created user
        # reresh contains both the refresh token and access token
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)