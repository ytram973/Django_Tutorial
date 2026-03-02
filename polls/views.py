# from django.shortcuts import render

# # Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from .models import Question ,Choice
from .forms import QuestionCreateForm
from django.template import loader
from django.views import generic
from django.db.models import Sum, Avg
from datetime import datetime
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajoute un formulaire vide si pas déjà présent
        if "form" not in context:
            context["form"] = QuestionCreateForm()
        return context

    def post(self, request):
        form = QuestionCreateForm(request.POST)
        
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        pub_date = form.cleaned_data["pub_date"]
        if timezone.is_naive(pub_date):
            pub_date = timezone.make_aware(pub_date, timezone.get_current_timezone())

        Question.objects.create(
            question_text=form.cleaned_data["question_text"],
            pub_date=pub_date
        )

        return HttpResponseRedirect(reverse("polls:index")) 
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "all_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")
    
class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object

        choices = question.choice_set.all()
        total_votes = choices.aggregate(total=Sum("votes"))["total"] or 0

        choices_data = []
        for c in choices:
            pct = (c.votes / total_votes * 100) if total_votes > 0 else 0
            choices_data.append((c.choice_text, c.votes, round(pct, 2)))

        context["choices"] = choices_data
        context["total_votes"] = total_votes
        return context


class StatisticsView(generic.TemplateView):
    template_name = "polls/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_polls = Question.objects.count()
        total_choices = Choice.objects.count()

        total_votes = Choice.objects.aggregate(
            total=Sum("votes")
        )["total"] or 0

        avg_votes_per_poll = (
            Question.objects
            .annotate(votes_sum=Sum("choice__votes"))
            .aggregate(avg=Avg("votes_sum"))["avg"]
            or 0
        )

        context["total_polls"] = total_polls
        context["total_choices"] = total_choices
        context["total_votes"] = total_votes
        context["avg_votes_per_poll"] = avg_votes_per_poll

        return context
    
def vote(request, question_id):
    question =get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        
        return render(
            request,
            "polls/detail.html",{
                "question":question,
                "error_message": "You didn't select a choice",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))