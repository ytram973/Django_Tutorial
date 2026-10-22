from django.db import transaction
from rest_framework import serializers

from .models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "choice_text")
        read_only_fields = fields


class PublicQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date", "choices")


class ChoiceWithVotesSerializer(ChoiceSerializer):
    class Meta(ChoiceSerializer.Meta):
        fields = ("id", "choice_text", "votes")
        read_only_fields = fields


class QuestionWithVotesSerializer(serializers.ModelSerializer):
    choices = ChoiceWithVotesSerializer(source="choice_set", many=True, read_only=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date", "choices", "total_votes")
        read_only_fields = fields

    def get_total_votes(self, question):
        return sum(choice.votes for choice in question.choice_set.all())


class QuestionCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=2,
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date", "choices")
        read_only_fields = ("id",)

    def validate_question_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("La question ne peut pas être vide.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        choices = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)
        Choice.objects.bulk_create(
            [Choice(question=question, choice_text=choice) for choice in choices]
        )
        return question


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(min_value=1)
