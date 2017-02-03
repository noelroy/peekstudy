from django import forms
from feeds.models import Feed


class PostForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ['post']