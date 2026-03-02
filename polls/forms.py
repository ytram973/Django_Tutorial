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

    def clean_question_text(self):
        value = self.cleaned_data["question_text"].strip()
        if not value:
            raise forms.ValidationError("La question ne peut pas être vide.")
        return value