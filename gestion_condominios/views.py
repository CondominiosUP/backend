""" Views for the REST API. """

# Django
from django.db.models import query
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Django REST Framework
from rest_framework import status, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
from .serializers import *

# Models
from .models import *

# Utils
from random import choice


class ShowAPI(APIView):
    """ Showing all the endpoints of the API. """
    permission_classes = [AllowAny,]

    def get(self, request):
        """ Handle HTTP Get request. """
        data = {
            'Endpoints': {
                'https://condominos-api.herokuapp.com/login/',
                'https://condominos-api.herokuapp.com/invite/',
                'https://condominos-api.herokuapp.com/names-condominiums/',
                'https://condominos-api.herokuapp.com/condominium-list/',
                'https://condominos-api.herokuapp.com/condominium/<int:pk>/',
                'https://condominos-api.herokuapp.com/condominium/priority-or-upgrade/',
                'https://condominos-api.herokuapp.com/condominium/priority-or-upgrade/<int:pk>/',
                'https://condominos-api.herokuapp.com/condominium/sugestions/',
                'https://condominos-api.herokuapp.com/financial-status/',
                'https://condominos-api.herokuapp.com/financial-status/<int:pk>/',
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    """ Users login API View (admin and users). """

    permission_classes = [AllowAny,]

    def post(self, request):
        """Handle HTTP Post request"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        username = UserBaseModelSerializer(user)
        data = {
            'token': token,
            'user': username.data,
        }
        return Response(data, status=status.HTTP_200_OK)


def create_email(email, subject, template_path, context):
    template = get_template(template_path)
    content = template.render(context)
    mail = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[email]
    )
    mail.attach_alternative(content, 'text/html')
    return mail

def generate_random_username_and_password():
    length = 10
    values = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
    username, password = "", ""
    username, password = username.join([choice(values) for i in range(length)]), password.join([choice(values) for i in range(length)])
    User.objects.create_user(username=username, password=password)
    data = []
    data.append({
        'username': username,
        'password': password,
        })
    return data


class InviteAPIView(APIView):
    """
    Invitation sent by an administrator to an user.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        """ Create an email to invite the new user. """
        temp = generate_random_username_and_password()
        print(request.data['email'])
        invitation_email = create_email(
            request.data['email'],
            'Invitación para unirse al condominio',
            'verify_account.html',
            {
                'username': temp[0]['username'],
                'password': temp[0]['password'],
            },
        )
        invitation_email.send(fail_silently=False)
        data=[]
        data.append(
            {"message":"Email sent succesfully"}
        )
        return Response(data, status=status.HTTP_200_OK)


class CondominiumListAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumModelSerializer
    
    def get(self, request):
        return self.list(request)


class FinancialStatusListAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CondominiumAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer


class NamesCondominiumsAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = NamesCondominiumsModelSerializer

    def get(self, request):
        return self.list(request)


class PostPriorityOrUpgradeAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumPriorityOrUpgradeModelSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetPriorityOrUpgradeAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PriorityOrUpgrade.objects.all()
    serializer_class = GetPriorityOrUpgradeByPKModelSerializer


class FinancialStatusRetriveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer


class SendSuggestionsAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSuggestionModelSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UpdateProfileView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSuggestionModelSerializer

    def get(self, request):
        return self.list(request)
    
    def update(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)