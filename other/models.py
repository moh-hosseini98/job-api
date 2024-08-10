from core.models import TimeStampedModel
from core.services import get_path_upload_image_company, validate_image_size
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings




class Company(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to=get_path_upload_image_company,
        validators=[validate_image_size],
        blank=True,
        default="default/company.png",
    )
    bio = models.TextField()
    company_url = models.URLField(blank=True)
    dou_url = models.URLField(blank=True)
    num_employees = models.PositiveIntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name