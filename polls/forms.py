from django import forms

class QuestionCreateForm(forms.Form):
    question_text = forms.CharField(
        max_length=200,
        required=True,
        label="Question",
        widget=forms.Textarea(attrs={"placeholder": "Votre question"})
    )

    pub_date = forms.DateTimeField(
        required=True,
        label="Date de publication",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    
    choice_1 = forms.CharField(
        max_length=200,
        required=True,
        label="Choix 1",
        widget=forms.TextInput(attrs={"placeholder": "Choix obligatoire"})
    )
    choice_2 = forms.CharField(
        max_length=200,
        required=False,
        label="Choix 2",
        widget=forms.TextInput(attrs={"placeholder": "Choix optionnel"})
    )
    choice_3 = forms.CharField(
        max_length=200,
        required=False,
        label="Choix 3",
        widget=forms.TextInput(attrs={"placeholder": "Choix optionnel"})
    )
    
    def clean_question_text(self):
        value = self.cleaned_data["question_text"].strip()
        if not value:
            raise forms.ValidationError("La question ne peut pas être vide.")
        return value
    
    def get_choices(self):
        choices = []
        for i in range(1, 4):
            choice_text = self.cleaned_data.get(f"choice_{i}", "").strip()
            if choice_text:
                choices.append(choice_text)
        return choices