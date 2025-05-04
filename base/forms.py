from django import forms
from .models import Project

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your password'
        })
    )


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter project name',
            'required': True
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full h-32',
            'placeholder': 'Enter project description',
            'required': True
        })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input input-bordered w-full',
            'type': 'date',
            'required': True
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input input-bordered w-full',
            'type': 'date',
            'required': True
        })
    )
    status = forms.ChoiceField(
        choices=Project.status_choices,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full',
            'required': True
        })
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data

