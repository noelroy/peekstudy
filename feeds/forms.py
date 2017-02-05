from django import forms
from feeds.models import Feed


class PostForm(forms.ModelForm):
    post_image = forms.ImageField()
    post = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=500)
    class Meta:
        model = Feed
        fields = ['post','post_image']