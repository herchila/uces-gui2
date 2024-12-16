import re

from django import forms


class CreateForm(forms.Form):
    question_text = forms.CharField(
        max_length=200,
        error_messages={"required": "El campo no puede estar vacío."},
    )

    def clean_question_text(self):
        question_text = self.cleaned_data.get("question_text")
        validate_question_text(question_text)
        return question_text


class UpdateForm(forms.Form):
    question_id = forms.IntegerField()
    question_text = forms.CharField(
        max_length=200,
        error_messages={"required": "El campo no puede estar vacío."},
    )

    def clean_question_text(self):
        question_text = self.cleaned_data.get("question_text")
        validate_question_text(question_text)
        return question_text
    
    def clean(self):
        cleaned_data = super().clean()
        question_id = cleaned_data.get("question_id")
        try:
            question_id = int(question_id)
        except Exception as e:
            print(f"[CrudForm] -> clean - Error: {e}")
            raise forms.ValidationError("Error inesperado.")
        
        return cleaned_data


class DeleteForm(forms.Form):
    question_id = forms.IntegerField()
    
    def clean_question_id(self):
        question_id = self.cleaned_data.get("question_id")
        try:
            question_id = int(question_id)
        except Exception as e:
            print(f"[CrudForm] -> clean - Error: {e}")
            raise forms.ValidationError("Error inesperado.")
        
        return question_id


def validate_question_text(question_text) -> None:
    if not question_text:
        raise forms.ValidationError("El campo no puede estar vacío.")

    if not re.match(r'^[a-zA-Z0-9\s]+$', question_text):
        raise forms.ValidationError("Solo se puede ingresar letras y espacios")
