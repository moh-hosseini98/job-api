from accounts.models import EMPLOY_OPTIONS, ENG_LEVEL, ContactCv
from core.models import TimeStampedModel
from other.models import Category, Company
from django.conf import settings
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager




class Vacancy(TimeStampedModel):
    """Vacancy Model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vacancy")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancy")
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.TextField(max_length=1000, validators=[MinLengthValidator(200)])
    requirements = models.TextField(max_length=1000, blank=True)
    other = models.TextField(max_length=1000, blank=True)
    eng_level = models.CharField(choices=ENG_LEVEL, max_length=50, default=ENG_LEVEL.none)
    salary = models.PositiveIntegerField(validators=[MaxValueValidator(100000)])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="vacancy")
    skills = TaggableManager(blank=True)
    work_exp = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True, null=True)
    employ_options = MultiSelectField(choices=EMPLOY_OPTIONS, max_length=50)

    is_test_task = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class VacancyView(TimeStampedModel):
    """Vacancy View Model"""

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="vacancy_views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="user_views")
    viewer_ip = models.GenericIPAddressField(null=True, blank=True)


    def __str__(self):
        return f"{self.vacancy.title} viewed by {self.user.first_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(cls, vacancy, user, viewer_ip):
        view, _ = cls.objects.get_or_create(vacancy=vacancy, user=user, viewer_ip=viewer_ip)
        view.save()


class Feedback(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="feedback_user")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="feedback_vacancy")
    contact_cv = models.ForeignKey(ContactCv, on_delete=models.SET_NULL, null=True, related_name="feedback_contact_cv")
    cover_letter = models.TextField(max_length=1000, null=True, blank=True)

    

    def __str__(self):
        return f"Feedback {self.user.first_name} - {self.vacancy.title}"


class Offer(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="offer_user")
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="candidate_offer")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="offer_vacancy")
    message = models.TextField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return f"Offer for {self.candidate.first_name} - {self.vacancy.title}"