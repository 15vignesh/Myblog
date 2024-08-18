from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    #usable_password=None
    class Meta:
        model=User
        fields=('email','username','password1','password2')
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # if 'usable_password' in self.fields:
        #     del self.fields['usable_password']
        self.fields.pop('usable_password',None)