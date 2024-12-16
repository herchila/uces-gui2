import re

from django import forms


class CrudForm(forms.Form):
    question_text = forms.CharField(
        max_length=200,
        error_messages={"required": "El campo no puede estar vacío."},
    )

    def clean_question_text(self):
        question_text = self.cleaned_data.get("question_text")
        if not question_text:
            raise forms.ValidationError("El campo no puede estar vacío.")

        if not re.match(r'^[a-zA-Z0-9\s]+$', question_text):
            raise forms.ValidationError("Solo se puede ingresar letras y espacios")

        return question_text
