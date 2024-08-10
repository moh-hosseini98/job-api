from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from .managers import CustomUserManager


TYPE_PROFILE_CHOICES = Choices(
    ("candidate",_("Candidate")),
    ("recruiter",_("Recruiter")),
)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom users model"""

    # User fields
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    type_profile = models.CharField(
        max_length=20,
        choices=TYPE_PROFILE_CHOICES,
        default=TYPE_PROFILE_CHOICES.candidate
    )


    # User permissions
    is_staff = models.BooleanField(default=False)  # For admin access
    is_active = models.BooleanField(default=True)  # For users activation

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = CustomUserManager()


    def __str__(self):
        """String representation of the user."""
        return self.email

    @property
    def get_full_name(self):
        """Returns the full name of the user."""
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        """Returns the short name of the user."""
        return self.first_name.title()

    @property
    def get_profile(self):
        """Returns the profile of the user."""
        if self.has_candidate_profile():
            return self.candidate_profile
        elif self.has_recruiter_profile():
            return self.recruiter_profile

    def has_candidate_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.candidate:
            return hasattr(self, "candidate_profile")
        return False

    def has_recruiter_profile(self):
        if self.type_profile == TYPE_PROFILE_CHOICES.recruiter:
            return hasattr(self, "recruiter_profile")
        return False    