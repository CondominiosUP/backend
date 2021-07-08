from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.fields.related import OneToOneField

class BaseModelCustom(models.Model):
    created_at = models.DateTimeField(
        'created at', 
        auto_now_add=True,
        help_text='Date time when the object was created.'
    )

    updated_at = models.DateTimeField(
        'modified at', 
        auto_now=True,
        help_text='Date time when the object was last modified.'
    )

    class Meta:
        """Meta option."""
        abstract = True


class Condominium(BaseModelCustom):
    name_condominium = models.CharField(max_length=200)

    def __str__(self):
        return self.name_condominium
    

class Department(BaseModelCustom):
    condominium_id    = models.ForeignKey(Condominium, related_name='departments', on_delete=models.CASCADE)
    department_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)], blank=False)
    department_block  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)], blank=False)
    number_habitants  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], blank=False, default=0)
    department_owner  = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'owner: {self.department_owner}, number: {self.department_number}, block: {self.department_block}'
    

class ProfileHabitant(BaseModelCustom):
    user                 = OneToOneField(User, on_delete=models.CASCADE)
    phone_regex          = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                           message="Phone number must be entered in the format: '999999999'. From 9 up to 15 digits allowed.")
    p_number             = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    p_number_emergency   = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    department_id        = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='department_id_owner')

    def __str__(self):
        return self.user.username
    

class Comment(BaseModelCustom):
    owner_department = models.CharField(max_length=100, blank=False)
    condominium_id   = models.ForeignKey(Condominium, related_name="condominium_suggestions", on_delete=models.CASCADE)
    comment_title    = models.CharField(max_length=100, blank=True)
    comment          = models.TextField(blank=True)
    flaw_title       = models.CharField(max_length=100, blank=True)
    flaw             = models.TextField(blank=True)

    def __str__(self):
        if self.comment_title == "" and self.flaw_title == "":
            return self.owner_department
        elif self.comment_title == "" and self.flaw_title != "":
            return f'{self.owner_department}, flaw title: {self.flaw_title}'
        elif self.comment_title != "" and self.flaw_title == "":
            return f'{self.owner_department}, comment title: {self.comment_title}'
        else:
            return f'{self.owner_department}, comment title: {self.comment_title}, flaw title: {self.flaw_title}'
    

class FinancialStat(BaseModelCustom):
    condominium_id  = models.ForeignKey(Condominium, related_name='financial_status' , on_delete=models.CASCADE)
    type_detail     = models.CharField(max_length=100, blank=False)
    income          = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    expenses        = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    details         = models.TextField(blank=False)

    def __str__(self):
        return f'{self.condominium_id.name_condominium}, detail: {self.type_detail}'

class PriorityOrUpgrade(BaseModelCustom):
    condominium_id = models.ForeignKey(Condominium, related_name="condominium_data", on_delete=models.CASCADE)
    name           = models.CharField(max_length=200, blank=False)
    detail         = models.TextField(blank=False)
    priority       = models.BooleanField(default=False)
    upgrade        = models.BooleanField(default=False)
    to_do          = models.BooleanField(default=True)
    doing          = models.BooleanField(default=False)
    done           = models.BooleanField(default=False)

    def __str__(self):
        return self.name