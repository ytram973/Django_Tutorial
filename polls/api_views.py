from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .api_serializers import (
    PublicQuestionSerializer,
    QuestionCreateSerializer,
    QuestionWithVotesSerializer,
    VoteSerializer,
)
from .models import Choice, Question


class PublicQuestionListView(generics.ListAPIView):
    queryset = Question.objects.prefetch_related("choice_set").order_by("-pub_date")
    serializer_class = PublicQuestionSerializer
    permission_classes = (AllowAny,)


class AuthenticatedQuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.prefetch_related("choice_set").order_by("-pub_date")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuestionCreateSerializer
        return QuestionWithVotesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        response_data = QuestionWithVotesSerializer(
            question, context=self.get_serializer_context()
        ).data
        return Response(response_data, status=status.HTTP_201_CREATED)


class VoteView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, question_id):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice = get_object_or_404(
            Choice,
            pk=serializer.validated_data["choice_id"],
            question_id=question_id,
        )
        Choice.objects.filter(pk=choice.pk).update(votes=F("votes") + 1)
        return Response(
            {"detail": "Vote enregistré.", "choice_id": choice.pk},
            status=status.HTTP_200_OK,
        )
