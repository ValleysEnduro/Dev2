from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Makes email required
    avatar = forms.ImageField(required=False)  # Ensures avatar is optional

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # This is somewhat redundant unless you have specific logic to handle
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user
