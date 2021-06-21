from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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

class AdminCondominium(BaseModelCustom, models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

class Condominium(BaseModelCustom, models.Model):
    administrator_id = models.ForeignKey(AdminCondominium, on_delete=models.CASCADE)

class Department(BaseModelCustom, models.Model):
    condominium_id    = models.OneToOneField(Condominium, on_delete=models.CASCADE)
    department_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)], blank=False)
    department_block  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)], blank=False)
    number_habitants  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], blank=False)
    department_owner  = models.CharField(max_length=200, blank=False)

class Department_owner(BaseModelCustom, models.Model):
    user_id              = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex          = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    p_number             = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    p_number_emergency   = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    department_id        = models.OneToOneField(Department, on_delete=models.CASCADE)
    account_confirmation = models.BooleanField(default=False)

class Comments(BaseModelCustom, models.Model):
    owner_id        = models.OneToOneField(Department_owner, on_delete=models.CASCADE)
    condominium_id  = models.OneToOneField(Condominium, on_delete=models.CASCADE)
    comment_title   = models.CharField(max_length=100, blank=False)
    comment         = models.TextField(blank=False)
    flaw_title      = models.CharField(max_length=100, blank=False)
    flaw            = models.TextField(blank=False)

class FinancialStatus(BaseModelCustom, models.Model):
    condominium_id = models.OneToOneField(Condominium, on_delete=models.CASCADE)
    type_detail    = models.CharField(max_length=100, blank=False)
    income         = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    expenses       = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    details        = models.TextField(blank=False)
