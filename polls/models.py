from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def get_choices(self):
        choices = self.choice_set.all()
        total_votes = sum(c.votes for c in choices)

        result = []
        for c in choices:
            pct = (c.votes / total_votes * 100) if total_votes > 0 else 0
            result.append((c.choice_text, c.votes, round(pct, 2)))

        return result, total_votes
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text