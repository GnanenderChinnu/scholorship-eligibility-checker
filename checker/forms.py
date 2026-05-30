from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import StudentProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ["user", "created_at", "updated_at"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "current_year": forms.NumberInput(attrs={"min": 1, "max": 8}),
            "has_disability": forms.CheckboxInput(),
            "is_orphan": forms.CheckboxInput(),
            "is_bpl": forms.CheckboxInput(),
            "has_bank_account": forms.CheckboxInput(),
            "aadhaar_linked_bank": forms.CheckboxInput(),
            "has_income_certificate": forms.CheckboxInput(),
            "has_caste_certificate": forms.CheckboxInput(),
            "has_disability_certificate": forms.CheckboxInput(),
        }
