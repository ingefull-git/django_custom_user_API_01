from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUser(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterUser, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')