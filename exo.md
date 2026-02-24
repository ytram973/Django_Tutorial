# 2.2 Exercices sur les parties 1 et 2

## 2.2.1


### 1 `polls/models.py`

### 2 `images/2.2.1-2`

### 3 oui oui oui oui

### 4 `polls/admin.py`

### 5: Non je ne peut pas car mon utilisateur na pas les droit dacceder au panel admin

### 6: Pour que utilisateur sois admin il faut cocher Statut équipe

### 7: Pour desactiver son compte il faut decocher Actif


## 2.2.2 exercice shell

### 2.2.2.2 Questions

### 1
```python
from polls.models import Question

for question in Question.objects.all():
    print(question.id, question.question_text, question.pub_date)

```
### 2 
```python
# by year
Question.objects.filter(pub_date__year=2026)

# by month
Question.objects.filter(pub_date__month=6)

# by day
Question.objects.filter(pub_date__day=1)
```
### 3 
```python

q =Question.objects.filter(pk=3)

print(q.id)
print(q.question_text)
print(q.pub_date)

q.choice_set.all()
```
### 4
```python
for question in Question.objects.all():
    print("Question :")
    print("Id:", question.id)
    print("Texte:", question.question_text)
    print("Date:", question.pub_date)
    
    print("Choix :")
    for choice in question.choice_set.all():
        print("   -", choice.choice_text, "| votes:", choice.votes)
    
    print("***********")
--------------------------------------------------------
>>> for question in Question.objects.all():
...     print("Question :")
...     print("Id:", question.id)
...     print("Texte:", question.question_text)
...     print("Date:", question.pub_date)
...     
...     print("Choix :")
...     for choice in question.choice_set.all():
...         print("   -", choice.choice_text, "| votes:", choice.votes)
...     
...     print("***********")
...
Question :
Id: 1
Texte: what's up?
Date: 2026-02-23 08:46:27+00:00
Choix :
   - Not much | votes: 0
   - The sky | votes: 0
***********
Question :
Id: 3
Texte: En Java, quelle est la différence principale entre une interface et une abstract class ?
Date: 2026-02-01 09:31:47+00:00
Choix :
   - Une interface peut contenir des méthodes implémentées, une classe abstraite ne peut pas | votes: 0
   - Une classe abstraite peut contenir des attributs d’instance, une interface non | votes: 0
   - Une interface ne peut pas être implémentée par plusieurs classes | votes: 0
***********
Question :
Id: 4
Texte: Quelle est la complexité moyenne d’accès (get) dans une HashMap en Java ?
Date: 2026-02-02 09:32:11+00:00
Choix :
***********
Question :
Id: 5
Texte: Quelle est votre techno préférée ?
Date: 2026-02-24 07:24:13.047665+00:00
Choix :
   - java | votes: 0
   - python | votes: 0
   - javaScript | votes: 0
***********
>>>
```
### 5
```python
for question in Question.objects.all():
    count = question.choice_set.count()
    print(question.question_text, "→", count, "choix")
-------------------------------------------------------------
>>> for question in Question.objects.all():
...     count = question.choice_set.count()
...     print(question.question_text, "→", count, "choix")
... 
what's up? → 2 choix
En Java, quelle est la différence principale entre une interface et une abstract class ? → 3 choix
Quelle est la complexité moyenne d’accès (get) dans une HashMap en Java ? → 0 choix
Quelle est votre techno préférée ? → 3 choix
>>>
```
### 7
```python
# ordre décroissant
questions = Question.objects.order_by("-pub_date")
# ordre croissant
questions = Question.objects.order_by("pub_date")

for q in questions:
    print(q.question_text, q.pub_date)

-----------------------------------------------------------------
>>> from polls.models import Question                                 
>>> questions = Question.objects.order_by("-pub_date")
>>> for q in questions:
...     print(q.question_text, q.pub_date)
... 
Quelle est votre techno préférée ? 2026-02-24 07:24:13.047665+00:00
what's up? 2026-02-23 08:46:27+00:00
Quelle est la complexité moyenne d’accès (get) dans une HashMap en Java ? 2026-02-02 09:32:11+00:00
En Java, quelle est la différence principale entre une interface et une abstract class ? 2026-02-01 09:31:47+00:00
>>>
```
### 9
```python
from polls.models import Question
from django.utils import timezone

q = Question.objects.create(
    question_text="Quelle est votre techno préférée ?",
    pub_date=timezone.now()
)
```

### 10
```python
from polls.models import Question, Choice
>>> q=Question.objects.get(pk=5)
>>> Choice.objects.create(question=q,choice_text="java",votes=0)
<Choice: java>
>>> Choice.objects.create(question=q,choice_text="python",votes=0)
<Choice: python>
>>> Choice.objects.create(question=q,choice_text="javaScript",votes=0)
<Choice: javaScript>
>>>
```

### 11
```python
>>> from polls.models import Question, Choice
>>> q = Question.objects.get(pk=5)
>>> q.was_published_recently()   
True
>>>
```

# 3 Tutoriel augmenté, parties 3 et 4