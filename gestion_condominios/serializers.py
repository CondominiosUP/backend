""" Serializers. """

# Django
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import fields
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from .models import Condominium, Department, FinancialStat, PriorityOrUpgrade, Comment


class UserLoginSerializer(serializers.Serializer):
    """ User Login serializers. """

    username = serializers.CharField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        """ Verify credentials. """
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """ Generate or retrieve new token. """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserBaseModelSerializer(serializers.ModelSerializer):
    """ User base model serializer. """
    class Meta:
        """ Meta class. """
        model  = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
        )


class DepartmentModelSerializer(serializers.ModelSerializer):
    """ Department model serializer. """

    class Meta:
        """ Meta class. """
        model  = Department
        fields = (
            'department_number',
            'department_block',
            'number_habitants',
            'department_owner'
        )


class CondominiumModelSerializer(serializers.ModelSerializer):
    """ Condominium model serializer. """

    departments = DepartmentModelSerializer(many=True)

    class Meta:
        """ Meta class. """
        model = Condominium
        fields = (
            'id',
            'name_condominium',
            'departments',
        )

class FinancialStatusModelSerializer(serializers.ModelSerializer):
    """ Financial status model serializer. """

    class Meta:
        """ Meta class. """
        model = FinancialStat
        fields = (
            'created_at',
            'type_detail',
            'income',
            'expenses',
            'details',
        )


class CondominiumStatusModelSerializer(serializers.ModelSerializer):
    """ Condominium status model serializer. """

    financial_status = FinancialStatusModelSerializer(many=True)

    class Meta:
        """ Meta class. """
        model = Condominium
        fields = (
            'id',
            'name_condominium',
            'financial_status',
        )
    
    def create(self, validated_data):
        financial_data = validated_data.pop('financial_status')
        try: 
            financial = Condominium.objects.get(name_condominium=validated_data['name_condominium'])
            for f_data in financial_data:
                FinancialStat.objects.create(condominium_id=financial, **f_data)
                return financial
        except ObjectDoesNotExist:
            raise serializers.ValidationError("The name of the condominium doesn't match with any of them.")
            

class NamesCondominiumsModelSerializer(serializers.ModelSerializer):
    """ Names list of condominiums model serializer. """
    class Meta:
        """ Meta class. """
        model = Condominium
        fields = (
            'id',
            'name_condominium',
        )

class GetPriorityOrUpgradeByPKModelSerializer(serializers.ModelSerializer):
    """ Get the priority or upgrade by a pk model serializer. """

    condominium_data = serializers.SerializerMethodField('get_data_from_condominium')

    class Meta:
        """ Meta class. """
        model = PriorityOrUpgrade
        fields = (
            'id',
            'name',
            'detail',
            'priority',
            'upgrade',
            'to_do',
            'doing',
            'done',
            'condominium_data'
        )

    def get_data_from_condominium(self, request):
        condominium_data = {
            'id': request.condominium_id.id,
            'name_condominium': request.condominium_id.name_condominium
        }
        return condominium_data


class PriorityOrUpgradeModelSerializer(serializers.ModelSerializer):
    """ Priority or upgrade model serializer. """
    class Meta:
        """ Meta class. """
        model = PriorityOrUpgrade
        fields = (
            'id',
            'name',
            'detail',
            'priority',
            'upgrade',
            'to_do',
            'doing',
            'done',
        )


class CondominiumPriorityOrUpgradeModelSerializer(serializers.ModelSerializer):
    """ Condominium priority or upgrade model serializer. """

    condominium_data = PriorityOrUpgradeModelSerializer(many=True)

    class Meta:
        """ Meta class. """
        model = Condominium
        fields = (
            'id',
            'name_condominium',
            'condominium_data',
        )
    
    def create(self, validated_data):
        detail_data = validated_data.pop('condominium_data')
        try: 
            detail = Condominium.objects.get(name_condominium=validated_data['name_condominium'])
            for d_data in detail_data:
                PriorityOrUpgrade.objects.create(condominium_id=detail, **d_data)
                return detail
        except ObjectDoesNotExist:
            raise serializers.ValidationError("The name of the condominium doesn't match with any of them.")


class SuggestionsModelSerializer(serializers.ModelSerializer):
    """ Suggestions model serializer. """
    
    class Meta:
        """ Meta class. """
        model = Comment
        fields = (
                'owner_department',
                'comment_title',
                'comment',
                'flaw_title',
                'flaw',
        )

    
class CondominiumSuggestionModelSerializer(serializers.ModelSerializer):
    """ Condominium suggestion model serializer. """
    condominium_suggestions = SuggestionsModelSerializer(many=True)

    class Meta:
        """ Meta class. """
        model = Condominium
        fields = (
            'id',
            'name_condominium',
            'condominium_suggestions',
        )

    def create(self, validated_data):
        suggestions_data = validated_data.pop('condominium_suggestions')
        try: 
            detail = Condominium.objects.get(name_condominium=validated_data['name_condominium'])
            for s_data in suggestions_data:
                Comment.objects.create(condominium_id=detail, **s_data)
                return detail
        except ObjectDoesNotExist:
            raise serializers.ValidationError("The name of the Condominium doesn't match with any of them.")