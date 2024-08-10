from rest_framework import generics, permissions, serializers
from taggit.models import Tag
from .models import Category, Company
from .serializers import CategorySerializer, CompanyUpdateSerializer, SkillsSerializer,CompanySerializer
from accounts.permissions import RecruiterRequiredPermission

class CategoryListAPIView(generics.ListAPIView):
    """List all categories. Pagination page size is 100."""

    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
   


class CompanyListAPIView(generics.ListAPIView):
    """List all companies, Pagination page size is 10. Public permission"""

    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class CompanyMyListCreateAPIView(generics.ListCreateAPIView):
    """List user companies and create new, Only 10 companies. Only recruiters can create and list companies."""

    # serializer_class = CompanySerializer
    permission_classes = [RecruiterRequiredPermission]


    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanySerializer
        return CompanyUpdateSerializer

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        user = self.request.user
        if Company.objects.filter(user=user).count() >= 10:
            raise serializers.ValidationError({"msg": "One Recruiter can only have 10 companies."})
        serializer.save(user=self.request.user)


class CompanyDetailAPIView(generics.RetrieveAPIView):
    """Retrieve view for company details. Public permission"""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class CompanyMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """CRUD view for company details. Only recruiters can update and delete."""

    serializer_class = CompanyUpdateSerializer
    permission_classes = [RecruiterRequiredPermission]

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


class SkillsListAPIView(generics.ListAPIView):
    """List all tags for skills. Pagination page size is 100. Public permission"""

    queryset = Tag.objects.order_by("name").all()
    serializer_class = SkillsSerializer
    permission_classes = [permissions.AllowAny]
    