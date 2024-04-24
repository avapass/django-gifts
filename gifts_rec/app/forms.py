from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth import authenticate
from .models import Questionnaire, Question, Answer

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = authenticate(None, username=username, password=password)
        if user is None:
            raise ValidationError("This user does not exist")
        else:
            self.authenticated_user = user
        return self.cleaned_data

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        questionnaire = Questionnaire.objects.first()
        questions = questionnaire.questions.all()

        for question in questions:
            choices = [(choice.id, choice.text) for choice in question.answers.all()]
            self.fields['question_{}'.format(question.id)] = forms.ChoiceField(
                label = question.text,
                choices = choices,
                widget = forms.RadioSelect
            )

class FriendRequestForm(forms.Form):
    friend_username = forms.CharField(label='Friend Username', max_length=150)