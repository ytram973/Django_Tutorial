from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date",)
    ordering = ("-pub_date",)
    search_fields = ("question_text",)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "votes", "question")
    list_filter = ("question",)
    ordering = ("-votes",)
    search_fields = ("choice_text",)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)