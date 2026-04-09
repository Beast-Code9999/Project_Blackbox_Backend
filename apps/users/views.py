from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
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
    
class LoginView(APIView):
    """
    POST api/users/login/
    Accepts email and password
    Returns user data with fresh JWT tokens when successful
    Authenticate users and return user object
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # use authenticate to compare hashed password
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                {'error' : 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # if user 
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
