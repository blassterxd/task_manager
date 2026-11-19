from django import forms

from .models import Task

DATETIME_FORMAT = '%Y-%m-%dT%H:%M'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format=DATETIME_FORMAT,
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Принимаем значение из HTML-поля datetime-local.
        self.fields['due_date'].input_formats = [
            DATETIME_FORMAT,
            '%Y-%m-%dT%H:%M:%S',
        ]