from django import forms
from feeds.models import Feed
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    post_image = forms.ImageField(label='Choose your image', required=False)
    post = forms.CharField(
        widget=PagedownWidget(attrs={'class': 'form-control'}),
        max_length=500)
    class Meta:
        model = Feed
        fields = ['post','post_image']