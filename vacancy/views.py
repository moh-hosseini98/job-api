from accounts.permissions import CandidateRequiredPermission, RecruiterRequiredPermission
from .serializers import (
    FeedbackSerializer,
    RetrieveMyVacancySerializer,
    UpdateVacancySerializer,
    VacancySerializer,
)
from .models import Feedback, Vacancy, VacancyView
from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class VacancyListAPIView(generics.ListAPIView):
    """Vacancy List. Public. Pagination page size is 15."""

    queryset = (
        Vacancy.objects.select_related("user", "company", "category", "user__recruiter_profile")
        .prefetch_related("skills", "vacancy_views", "feedback_vacancy")
        .all()
    )
    serializer_class = VacancySerializer
    permission_classes = [permissions.AllowAny]


class VacancyMyListCreateAPIView(generics.ListCreateAPIView):
    """Vacancy My List. Only recruiters can create and list vacancies. Pagination page size is 10."""

    serializer_class = VacancySerializer
    permission_classes = [RecruiterRequiredPermission]

    def get_queryset(self):
        return (
            Vacancy.objects.select_related("user", "company", "category", "user__recruiter_profile")
            .prefetch_related("skills", "vacancy_views", "feedback_vacancy")
            .filter(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VacancySerializer
        return UpdateVacancySerializer

    def perform_create(self, serializer):
        user = self.request.user
        recruiter_profile = self.request.user.recruiter_profile
        if recruiter_profile.company:
            serializer.save(user=user, company=recruiter_profile.company)
        else:
            raise ValidationError({"error": "You do not have any company"})


class VacancyMyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vacancy Detail API. Only recruiters can update and delete vacancies."""

    lookup_field = "slug"
    permission_classes = [RecruiterRequiredPermission]

    def get_queryset(self):
        return Vacancy.objects.select_related("user", "company", "category").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveMyVacancySerializer
        return UpdateVacancySerializer


class VacancyDetailAPIView(generics.RetrieveAPIView):
    """Vacancy Detail API. Public."""

    queryset = Vacancy.objects.select_related("user", "company", "category").all()
    lookup_field = "slug"
    serializer_class = VacancySerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # TODO: some kind of caching
        # if user.is_authenticated and user.has_candidate_profile():
        viewer_ip = request.META.get("REMOTE_ADDR", None)
        # TODO: change when using only Docker and Celery Maybe
        VacancyView.record_view(vacancy=instance, user=None, viewer_ip=viewer_ip)
        # create_vacancy_view.delay(instance.id, user.id, viewer_ip)

        return Response(serializer.data)


class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    """Feedback List Create. Recruiter can GET feedback list of vacancy. Candidate can POST feedback.
    After creating feedback, is created ChatRoom and ChatMessage. Pagination page size is 10."""

    serializer_class = FeedbackSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = (
            Feedback.objects.select_related("user", "user__candidate_profile", "vacancy", "vacancy__company")
            .prefetch_related("contact_cv", "user__candidate_profile__skills", "user__candidate_profile__category")
            .filter(vacancy__slug=self.kwargs["slug"])
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        vacancy = get_object_or_404(Vacancy, slug=self.kwargs["slug"])
        if Feedback.objects.filter(user=user, vacancy=vacancy).exists():
            raise serializers.ValidationError({"message": "Feedback already exists"})
        serializer.save(user=user, vacancy=vacancy, contact_cv=user.contact_cv)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [CandidateRequiredPermission]
        elif self.request.method == "GET":
            self.permission_classes = [RecruiterRequiredPermission]
        return super().get_permissions()