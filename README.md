2.2 Exercices sur les parties 1 et 2

5: non je ne peut pas



```python
py manage.py shell

from polls.models import Question

for question in Question.objects.all():
    print(question.id, question.question_text, question.pub_date)

```