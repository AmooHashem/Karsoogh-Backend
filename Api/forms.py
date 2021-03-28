from django import forms

from Api.models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer', 'file']
