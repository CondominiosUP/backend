""" Views for the REST API. """

# Django
from django.db.models import query
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Django REST Framework
from rest_framework import status, generics, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.renderers import JSONRenderer
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
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny,]

    def get(self, request):
        """ Handle HTTP Get request. """
        data = {
            'Endpoints': {
                'https://cb9e26a7474b.ngrok.io/v1/login/',
                'https://cb9e26a7474b.ngrok.io/v1/register-and-invite/',
                'https://cb9e26a7474b.ngrok.io/v1/names-condominiums/',
                'https://cb9e26a7474b.ngrok.io/v1/condominium-list/',
                'https://cb9e26a7474b.ngrok.io/v1/condominium/<int:pk>/',
                'https://cb9e26a7474b.ngrok.io/v1/condominium/priority-or-upgrade/',
                'https://cb9e26a7474b.ngrok.io/v1/condominium/priority-or-upgrade/<int:pk>/',
                'https://cb9e26a7474b.ngrok.io/v1/condominium/sugestions/',
                'https://cb9e26a7474b.ngrok.io/v1/financial-status/',
                'https://cb9e26a7474b.ngrok.io/v1/financial-status/<int:pk>/',
                'https://cb9e26a7474b.ngrok.io/v1/update/<int:pk>/',
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    """ Users login API View (admin and users). """
    renderer_classes = [JSONRenderer]
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


class CondominiumListAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumModelSerializer
    
    def get(self, request):
        return self.list(request)


class FinancialStatusListAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CondominiumAPIView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer


class NamesCondominiumsAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = NamesCondominiumsModelSerializer

    def get(self, request):
        return self.list(request)


class PostPriorityOrUpgradeAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumPriorityOrUpgradeModelSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetPriorityOrUpgradeAPIView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = PriorityOrUpgrade.objects.all()
    serializer_class = GetPriorityOrUpgradeByPKModelSerializer


class FinancialStatusRetriveAPIView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumStatusModelSerializer


class SendSuggestionsAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSuggestionModelSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UpdatePasswordAPIView(generics.UpdateAPIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Password change successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class InviteAPIView(APIView):
    """
    Invitation sent by an administrator to an user.
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAdminUser]

    def post(self, request):
        """ Create an email to invite the new user. """
        data_user = User.objects.create(
            username = request.data['username'],
            email    = request.data['email'],
            first_name = request.data['name_owner'],
        )
        data_user.save()
        data_user_password = User.objects.get(pk=data_user.pk)
        data_user_password.set_password(request.data['password'])
        data_user_password.save()
        
        data_condominium = Condominium.objects.get(name_condominium=request.data['name_condominium'])
        data_department = Department.objects.create(
            condominium_id = data_condominium,
            department_number = request.data['number_department'],
            department_block = request.data['number_block'],
            number_habitants = request.data['number_habitants'],
            department_owner = request.data['name_owner']
        )
        data_department.save()

        user_data = User.objects.get(username=request.data['username'])
        department_data = Department.objects.get(department_owner=request.data['name_owner'])
        data_profile = ProfileHabitant.objects.create(
            user = user_data,
            p_number = request.data['p_number'],
            p_number_emergency = request.data['p_number_emergency'],
            department_id =department_data
        )
        data_profile.save()
        user_serializer = UserBaseModelSerializer(data_user)
        department_serializer = DepartmentModelSerializer(data_department)
        profile_serializer = ProfileUserModelSerializer(data_profile)
        condominium_name = BaseCondominiumModelSerializer(data_condominium)
        invitation_email = create_email(
            request.data['email'],
            'Invitación para unirse al condominio',
            'verify_account.html',
            {
                'username': request.data['username'],
                'password': request.data['password'],
            },
        )
        invitation_email.send(fail_silently=False)
        final_data = {
            "message": "Email sent succesfully",
            "user" : user_serializer.data,
            "profile": profile_serializer.data,
            "department": department_serializer.data,
            "condominium": condominium_name.data
        }
        return Response(final_data, status=status.HTTP_201_CREATED)