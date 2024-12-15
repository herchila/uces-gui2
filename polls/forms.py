from django import forms

class CrudForm(forms.Form):
    question_text = forms.CharField(max_length=200)

    def clean_question_text(self):
        question_text = self.cleaned_data.get("question_text")
        if not question_text:
            raise forms.ValidationError("El campo no puede estar vacío.")

        return question_text
