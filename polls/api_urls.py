from django.urls import path

from . import api_views

app_name = "polls_api"

urlpatterns = [
    path("polls/", api_views.PublicQuestionListView.as_view(), name="poll-list"),
    path("polls/<int:question_id>/vote/", api_views.VoteView.as_view(), name="vote"),
    path("manage/polls/", api_views.AuthenticatedQuestionListCreateView.as_view(), name="manage-polls"),
]
