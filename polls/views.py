# from django.shortcuts import render

# # Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from .models import Question ,Choice
from .forms import QuestionCreateForm
from django.template import loader
from django.views import generic
from django.db.models import F, Count, Sum, Avg
from datetime import datetime, timedelta
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        question = Question.objects.create(
            question_text=form.cleaned_data["question_text"],
            pub_date=pub_date
        )
        for choice_text in form.get_choices():
            Choice.objects.create(question=question, choice_text=choice_text)
            
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


class QuerySetView(generic.TemplateView):
    template_name = "polls/queryset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        context["q"]      = q
        context["search"] = self.request.GET.get("search", "").strip()

        method  = getattr(self, f"query_{q}", None)
        snippet = getattr(self, f"snippet_{q}", None)
        sql     = getattr(self, f"sql_{q}", None)

        if method:
            context["result"]  = method(context)
            context["snippet"] = snippet() if snippet else ""
            context["sql"]     = sql() if sql else ""

        return context

    # ── 1. Sondages déjà publiés
    def query_1(self, ctx):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")

    def snippet_1(self):
        return "Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')"

    def sql_1(self):
        return """SELECT *
FROM polls_question
WHERE pub_date <= '2026-03-04 12:00:00'
ORDER BY pub_date DESC"""

    # ── 2. Recherche icontains
    def query_2(self, ctx):
        terme = ctx["search"]
        if not terme:
            return Question.objects.none()
        return Question.objects.filter(
            question_text__icontains=terme
        ).order_by("-pub_date")

    def snippet_2(self):
        return "Question.objects.filter(question_text__icontains='<terme>')"

    def sql_2(self):
        return """SELECT *
FROM polls_question
WHERE UPPER(question_text) LIKE UPPER('%terme%')
ORDER BY pub_date DESC"""

    # ── 3. Questions sans aucun choix
    def query_3(self, ctx):
        return Question.objects.filter(choice__isnull=True)

    def snippet_3(self):
        return "Question.objects.filter(choice__isnull=True)"

    def sql_3(self):
        return """SELECT polls_question.*
FROM polls_question
LEFT JOIN polls_choice
    ON polls_choice.question_id = polls_question.id
WHERE polls_choice.id IS NULL"""

    # ── 4. Nombre de choix par sondage
    def query_4(self, ctx):
        return (
            Question.objects
            .annotate(nb_choices=Count("choice"), total_votes=Sum("choice__votes"))
            .order_by("-nb_choices")
        )

    def snippet_4(self):
        return "Question.objects.annotate(nb_choices=Count('choice'), total_votes=Sum('choice__votes')).order_by('-nb_choices')"

    def sql_4(self):
        return """SELECT
    polls_question.*,
    COUNT(polls_choice.id)   AS nb_choices,
    SUM(polls_choice.votes)  AS total_votes
FROM polls_question
LEFT JOIN polls_choice
    ON polls_choice.question_id = polls_question.id
GROUP BY polls_question.id
ORDER BY nb_choices DESC"""

    # ── 5. Le choix le plus voté global
    def query_5(self, ctx):
        best = Choice.objects.order_by("-votes").select_related("question").first()
        return [best] if best else []

    def snippet_5(self):
        return "Choice.objects.order_by('-votes').select_related('question').first()"

    def sql_5(self):
        return """SELECT
    polls_choice.*,
    polls_question.*
FROM polls_choice
INNER JOIN polls_question
    ON polls_question.id = polls_choice.question_id
ORDER BY polls_choice.votes DESC
LIMIT 1"""

    # ── 6. Choix jamais votés
    def query_6(self, ctx):
        return Choice.objects.filter(votes=0).select_related("question")

    def snippet_6(self):
        return "Choice.objects.filter(votes=0).select_related('question')"

    def sql_6(self):
        return """SELECT
    polls_choice.*,
    polls_question.*
FROM polls_choice
INNER JOIN polls_question
    ON polls_question.id = polls_choice.question_id
WHERE polls_choice.votes = 0"""

    # ── 7. Sondages avec au moins 5 votes
    def query_7(self, ctx):
        return (
            Question.objects
            .annotate(total=Sum("choice__votes"))
            .filter(total__gte=5)
            .order_by("-total")
        )

    def snippet_7(self):
        return "Question.objects.annotate(total=Sum('choice__votes')).filter(total__gte=5)"

    def sql_7(self):
        return """SELECT
    polls_question.*,
    SUM(polls_choice.votes) AS total
FROM polls_question
LEFT JOIN polls_choice
    ON polls_choice.question_id = polls_question.id
GROUP BY polls_question.id
HAVING SUM(polls_choice.votes) >= 5
ORDER BY total DESC"""

    # ── 8. Questions publiées cette semaine
    def query_8(self, ctx):
        since = timezone.now() - timedelta(days=7)
        return Question.objects.filter(pub_date__gte=since).order_by("-pub_date")

    def snippet_8(self):
        return "Question.objects.filter(pub_date__gte=timezone.now() - timedelta(days=7))"

    def sql_8(self):
        return """SELECT *
FROM polls_question
WHERE pub_date >= '2026-02-25 12:00:00'
ORDER BY pub_date DESC"""

    # ── 9. Reset votes — update() en masse
    def query_9(self, ctx):
        first = Question.objects.first()
        if not first:
            return []
        updated = Choice.objects.filter(question=first).update(votes=0)
        return [{"question": first, "updated": updated}]

    def snippet_9(self):
        return "Choice.objects.filter(question=q).update(votes=0)"

    def sql_9(self):
        return """UPDATE polls_choice
SET votes = 0
WHERE question_id = 1"""

    # ── 10. Classement par popularité
    def query_10(self, ctx):
        return (
            Question.objects
            .annotate(total_votes=Sum("choice__votes"))
            .order_by(F("total_votes").desc(nulls_last=True))
        )

    def snippet_10(self):
        return "Question.objects.annotate(total_votes=Sum('choice__votes')).order_by(F('total_votes').desc(nulls_last=True))"

    def sql_10(self):
        return """SELECT
    polls_question.*,
    SUM(polls_choice.votes) AS total_votes
FROM polls_question
LEFT JOIN polls_choice
    ON polls_choice.question_id = polls_question.id
GROUP BY polls_question.id
ORDER BY total_votes DESC NULLS LAST"""

    # ── 11. Sondages avec exactement 1 choix
    def query_11(self, ctx):
        return (
            Question.objects
            .annotate(nb=Count("choice"))
            .filter(nb=1)
        )

    def snippet_11(self):
        return "Question.objects.annotate(nb=Count('choice')).filter(nb=1)"

    def sql_11(self):
        return """SELECT
    polls_question.*,
    COUNT(polls_choice.id) AS nb
FROM polls_question
LEFT JOIN polls_choice
    ON polls_choice.question_id = polls_question.id
GROUP BY polls_question.id
HAVING COUNT(polls_choice.id) = 1"""

    # ── 12. Sondages qui ont des choix (Exclusion des vides)
    def query_12(self, ctx):
        return Question.objects.exclude(choice__isnull=True).distinct()

    def snippet_12(self):
        return "Question.objects.exclude(choice__isnull=True)"

    def sql_12(self):
        return """SELECT DISTINCT polls_question.*
FROM polls_question
INNER JOIN polls_choice
    ON polls_choice.question_id = polls_question.id"""