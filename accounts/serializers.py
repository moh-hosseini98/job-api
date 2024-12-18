from .models import EMPLOY_OPTIONS, CandidateProfile, ContactCv, RecruiterProfile
from core.serializers import CustomMultipleChoiceField
from other.serializers import ShortCompanySerializer
from other.models import Category, Company
from vacancy.models import Offer, Vacancy
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField


class CandidateProfileSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    # employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "category",
            "skills",
            "work_exp",
            "work_exp_bio",
            "salary_expectation",
            "city",
            "eng_level",
            "employ_options",
            "image",
            "find_job",
            "created_at",
            "updated_at",
        )


class CandidateProfileListSerializer(CandidateProfileSerializer):
    find_job = serializers.CharField(source="get_find_job_display", read_only=True)
    eng_level = serializers.CharField(source="get_eng_level_display", read_only=True)


class OfferSerializer(serializers.ModelSerializer):
    vacancy = serializers.SlugRelatedField(slug_field="slug", queryset=Vacancy.objects.all())

    class Meta:
        model = Offer
        fields = (
            "id",
            "vacancy",
            "message",
            "created_at",
            "updated_at",
        )


class UpdateCandidateProfileSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    employ_options = CustomMultipleChoiceField(choices=EMPLOY_OPTIONS)
    skills = TagListSerializerField()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "category",
            "skills",
            "work_exp",
            "work_exp_bio",
            "salary_expectation",
            "city",
            "eng_level",
            "employ_options",
            "image",
            "find_job",
        )


class UpdateCandidateProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ("image",)


class ShortCandidateProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "image",
        )


class RecruiterProfileSerializer(serializers.ModelSerializer):
    trust_hr = serializers.BooleanField(read_only=True)
    company = ShortCompanySerializer(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "company",
            "image",
            "trust_hr",
            "created_at",
            "updated_at",
        )


class UpdateRecruiterProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = ("image",)


class ShortRecruiterProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RecruiterProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "position",
            "image",
            "trust_hr",
        )


class UpdateRecruiterProfileSerializer(RecruiterProfileSerializer):
    company = serializers.SlugRelatedField(slug_field="name", queryset=Company.objects.all())


class ContactCvSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = ContactCv
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "telegram_url",
            "linkedin_url",
            "git_hub_url",
            "portfolio_url",
            "cv_file",
            "created_at",
            "updated_at",
        )


class UpdateContactCvFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCv
        fields = ("cv_file",)