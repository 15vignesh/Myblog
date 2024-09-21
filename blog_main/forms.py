from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blogs.models import Security
class RegistrationForm(UserCreationForm):
    #usable_password=None
    security_question = forms.CharField(max_length=255, help_text="Enter your security question")
    security_answer = forms.CharField(max_length=255, help_text="Enter the answer to your security question")

    class Meta:
        model=User
        fields=('email','username','password1','password2')
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # if 'usable_password' in self.fields:
        #     del self.fields['usable_password']
        self.fields.pop('usable_password',None)
    def save(self, commit=True):
        user = super().save(commit=False)  # Save the user object but don't commit to the database yet
        if commit:
            user.save()  # Now save the user instance
            # After saving the user, create the related Security instance
            security=Security.objects.create(
                user=user,
                security_question=self.cleaned_data.get('security_question'),
            )
            security.set_security_answer(self.cleaned_data.get('security_answer'))
            security.save()
        return user
class ForgotPasswordForm(forms.Form):
    username_or_email=forms.CharField(max_length=255,label="Username or Email")

class SecurityCheckForm(forms.Form):
    security_question=forms.CharField(max_length=255,label="Security Question")
    security_answer=forms.CharField(max_length=255,label="Security Answer",widget=forms.PasswordInput)
