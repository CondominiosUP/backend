from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowAPI.as_view(), name='show-api'), # GET only
    path('login/', UserLoginAPIView.as_view(), name='login'), # POST only
    path('invite/', InviteAPIView.as_view(), name='invite_user'), # POST only
    path('names-condominiums/', NamesCondominiumsAPIView.as_view(), name="list-names" ), # GET only
    path('condominium-list/', CondominiumListAPIView.as_view(), name="condominium-list"), # GET only
    path('condominium/<int:pk>/', CondominiumAPIView.as_view(), name="condominium"), # GET only
    path('condominium/priority-or-upgrade/', PostPriorityOrUpgradeAPIView.as_view(), name="priority-or-update"), # POST and GET only
    path('condominium/priority-or-upgrade/<int:pk>/', GetPriorityOrUpgradeAPIView.as_view(), name="get-priority-or-update"), # GET only
    path('condominium/sugestions/', SendSuggestionsAPIView.as_view(), name="suggestions"), # GET and POST only
    path('financial-status/', FinancialStatusListAPIView.as_view(), name="financial-status"), # POST and GET only
    path('financial-status/<int:pk>/', FinancialStatusRetriveAPIView.as_view(), name="financial-status-retrive"), # GET only
    # path('update/', UpdateProfileView.as_view(), name='update_profile'),

]