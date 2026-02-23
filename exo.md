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

