from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from api.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user is None:
            raise AuthenticationFailed("Invalid username or password. Please try again.")
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    if not data.get('name'):
        return Response({'detail': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not data.get('email'):
        return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not data.get('password'):
        return Response({'detail': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=data['email']).exists():
        return Response({'detail': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try:
        user = request.user
        data = request.data
        user.first_name = data.get('name', user.first_name)
        user.username = data.get('email', user.username)
        user.email = data.get('email', user.email)

        if data.get('password', '') != '':
            user.password = make_password(data['password'])

        user.save()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk=None):
    if pk is None:
        return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        message = {'detail': 'User not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    if pk is None:
        return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=pk)
        data = request.data

        user.first_name = data.get('name', user.first_name)
        user.username = data.get('email', user.username)
        user.email = data.get('email', user.email)
        user.is_staff = data.get('isAdmin', user.is_staff)

        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        message = {'detail': 'User not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    if pk is None:
        return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userForDeletion = User.objects.get(id=pk)
        userForDeletion.delete()
        return Response({'detail': 'User was deleted'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        message = {'detail': 'User not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        message = {'detail':f'{str(e)}'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
