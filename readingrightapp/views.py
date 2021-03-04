import jwt
from django.conf import settings

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Post
from .serializers import PostSerializer,PostjsonSerializer
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self,request):
        user = get_user_model()
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
            
        try:
            key = settings.SECRET_KEY
            payload = jwt.decode( refresh_token, key, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('expired refresh_token token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        serialized_user = UserSerializer(user).data

class PostjsonView(ListAPIView):
    queryset=''
    def list(self,request):
        user = get_user_model()
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')  
        try:
            key = settings.SECRET_KEY
            payload = jwt.decode( refresh_token, key, algorithms=['HS256'])
            query = Post.objects.all()
            serializer = PostjsonSerializer(list(query),many=True)
            result = serializer.data
            return Response(result)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('expired refresh_token token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        serialized_user = UserSerializer(user).data    
        

class DemoView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        return Response({'success':"Hurray you are authenticated"})