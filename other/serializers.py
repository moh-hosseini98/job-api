from .models import Category, Company
from rest_framework import serializers
from taggit.models import Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name",]


class ShortCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["id", "name", "image", "bio", "company_url",]


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "image",
            "bio",
            "company_url",
            "dou_url",
            "num_employees",
            "created_at",
        ]

class CompanySerializer(CompanyUpdateSerializer):
    pass      


class SkillsSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source="name")

    class Meta:
        model = Tag
        fields = ["id", "text"]