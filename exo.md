# 2.2 Exercices sur les parties 1 et 2

## 2.2.1

#### 5: Non je ne peut pas car mon utilisateur na pas les droit dacceder au panel admin

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
Question.objects.filter(pub_date__year=2025)

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

```
### 5
```python
for question in Question.objects.all():
    count = question.choice_set.count()
    print(question.question_text, "→", count, "choix")

```
### 7
```python
# ordre décroissant
questions = Question.objects.order_by("-pub_date")
# ordre croissant
questions = Question.objects.order_by("pub_date")

for q in questions:
    print(q.question_text, q.pub_date)

```