from django import forms
from .models import QuestionPaper

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ["title", "subject", "course", "year","file","difficulty"]
    
    def __init__(self, *args, **kwargs):
        super(QuestionPaperForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Bootstrap form control class
                'placeholder': f'Enter {field_name.replace("_", " ").title()}'
            })
