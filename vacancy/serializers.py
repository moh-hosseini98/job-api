from accounts.serializers import (
    CandidateProfileSerializer,
    ContactCvSerializer,
    ShortRecruiterProfileSerializer,
)
from accounts.models import EMPLOY_OPTIONS
from core.serializers import CustomMultipleChoiceField
from other.serializers import ShortCompanySerializer
from other.models import Category, Company
from .models import Feedback, Vacancy
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

class MyVacancySerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    skills = TagListSerializerField()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    company = serializers.SlugRelatedField(slug_field="name", queryset=Company.objects.all())
    recruiter = serializers.SerializerMethodField()
    views = serializers.IntegerField(source="vacancy_views.count", read_only=True)
    feedback = serializers.IntegerField(source="feedback_vacancy.count", read_only=True)
    is_user_feedback = serializers.SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "recruiter",
            "company",
            "title",
            "slug",
            "description",
            "requirements",
            "other",
            "eng_level",
            "salary",
            "category",
            "skills",
            "work_exp",
            "employ_options",
            "is_test_task",
            "views",
            "feedback",
            "is_user_feedback",
            "created_at",
            "updated_at",
        )
        depth = 1

    @extend_schema_field(ShortRecruiterProfileSerializer)
    def get_recruiter(self, obj):
        return ShortRecruiterProfileSerializer(
            obj.user.recruiter_profile, context={"request": self.context["request"]}, many=False
        ).data

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_user_feedback(self, obj):
        if not self.context["request"].user.is_authenticated:
            return False
        return Feedback.objects.filter(user=self.context["request"].user, vacancy=obj).exists()


class UpdateVacancySerializer(MyVacancySerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)


class RetrieveMyVacancySerializer(MyVacancySerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    company = ShortCompanySerializer(read_only=True, many=False)


class VacancySerializer(UpdateVacancySerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    eng_level = serializers.CharField(source="get_eng_level_display", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    company = ShortCompanySerializer(read_only=True, many=False)


class ShortVacancySerializer(UpdateVacancySerializer):
    class Meta:
        model = Vacancy
        fields = (
            "slug",
            "title",
            "company",
            "employ_options",
            "created_at",
            "updated_at",
        )


class FeedbackSerializer(serializers.ModelSerializer):
    candidate = serializers.SerializerMethodField()
    contact_cv = ContactCvSerializer(read_only=True, many=False)
    vacancy = ShortVacancySerializer(read_only=True, many=False)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "candidate",
            "vacancy",
            "contact_cv",
            "cover_letter",
            "created_at",
            "updated_at",
        )

    @extend_schema_field(CandidateProfileSerializer)
    def get_candidate(self, obj):
        return CandidateProfileSerializer(
            obj.user.candidate_profile, context={"request": self.context["request"]}, many=False
        ).data


class ShortFeedbackSerializer(FeedbackSerializer):
    contact_cv = ContactCvSerializer(read_only=True, many=False)

    class Meta:
        model = Feedback
        fields = (
            "vacancy",
            "contact_cv",
        )