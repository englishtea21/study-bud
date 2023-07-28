from django.forms import ModelForm
from django import forms
from .models import User, Room, Topic
from django.contrib.auth.forms import UserCreationForm
from dal import autocomplete


# для кастомной модели пользователя нужно менять форму регистрации
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    # name = forms.TextInput()
    # description = forms.TextInput()
    # topics = forms.ModelMultipleChoiceField(
    #     required=True,
    #     queryset=Topic.objects.all(),
    #     widget=forms.SelectMultiple(
    #         attrs={'data-placeholder': 'Search for items...'}),
    # )

    class Meta:
        model = Room
        fields = '__all__'
        # exclude = ['host', 'participants']
        widgets = {
            'topics': autocomplete.ModelSelect2Multiple(
                url='topic-autocomplete',
                attrs={
                    # Set some placeholder
                    'data-placeholder': 'Start typing ...',
                    # Only trigger autocompletion after 3 characters have been typed
                    'data-minimum-input-length': 1,
                },
            )
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'name', 'username', 'email', 'bio']
