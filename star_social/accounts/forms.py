from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    """A Django form for creating a User instance."""
    class Meta:

        fields = ('username', 'email', 'password1', 'password2')
        # get the Model that represents a User model in this project.
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setting custom labels for form field.
        self.fields['username'].label = "User Name"
        self.fields['email'].label = 'Email ID'