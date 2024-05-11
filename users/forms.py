# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Makes email required
    avatar = forms.ImageField(required=False)  # Ensures avatar is optional

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'avatar',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user

class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='Select an avatar', required=False)

    class Meta:
        model = CustomUser
        fields = ['avatar']
