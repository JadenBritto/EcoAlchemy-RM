from django import forms
from .models import ConsultationCase, CaseComment

class ConsultationCaseForm(forms.ModelForm):
    class Meta:
        model = ConsultationCase
        fields = ['title', 'waste_listing', 'description']

class CaseCommentForm(forms.ModelForm):
    class Meta:
        model = CaseComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }