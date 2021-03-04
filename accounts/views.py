import jwt
from django.conf import settings

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

class RegisterView(APIView):
    
    def post(self,request):
        first_name = request.data['firstname']
        last_name = request.data['lastname']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password1']
        password2 = request.data['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User(first_name=first_name,last_name=last_name,username=username,email=email)
                user.set_password(password) 
                user.save()
                refresh_token = RefreshToken.for_user(user)
                messages.info(request,'Registered Successfully!')
                return Response({
                    'status':"success", 
                    'user_id' :user.id, 
                    'refresh_token':str(refresh_token) , 
                    'access': str(refresh_token.access_token)
                })
        else:
            messages.info(request,'Passwords not matching')
            return redirect('register')
            
    def get(self,request):
        return render(request,"signup.html")

class LoginView(APIView):
    
    def post(self,request):
        User = get_user_model()
        username = request.data['username']
        password = request.data['password']
        response = Response()

        if (username is None) or (password is None):
            messages.info (request,'username and password required')
            return redirect('login')
        
        user = User.objects.filter(username=username).first()
    
        if(user is None):
            messages.info (request, 'user not found')
            return redirect('login')

        if (not user.check_password(password)):
            messages.info (request,'wrong password')
            return redirect('login')

        serialized_user = UserSerializer(user).data
        refresh_token = RefreshToken.for_user(user)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'status':"success", 
            'user_id' : user.id, 
            'user': serialized_user,
            'refresh_token': str(refresh_token) , 
            'access': str(refresh_token.access_token)
        }
        response.headers = {'Authorization': 'Token '+str(refresh_token.access_token)}
        return response
    def get(self,request):
        return render(request,"login.html")

class UserView(APIView):
    def get(self,request):
        user = get_user_model()
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            key = settings.SECRET_KEY
            payload = jwt.decode(
                refresh_token, key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh_token token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        serialized_user = UserSerializer(user).data
        response = Response()
        response.data = {
            'user': serialized_user 
        }
        return response
