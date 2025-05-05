from django import forms
from .models import Project, Profile
from django.contrib.auth.models import User

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
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status']

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
   
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', "End date must be after start date")
        
        return cleaned_data

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirm your password'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your username'
        })
    )
    role = forms.ChoiceField(
        choices=Profile.roles,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your phone number (optional)'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            # Create associated profile
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone']
            )
        return user



