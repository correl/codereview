from django import forms
from codereview.review.models import *

class NewReviewForm(forms.Form):
    author = forms.IntegerField(widget=forms.HiddenInput)
    repo = forms.IntegerField(widget=forms.HiddenInput)
    ref = forms.CharField(widget=forms.HiddenInput)
    parent = forms.CharField(widget=forms.HiddenInput, required=False)
    description = forms.CharField(widget=forms.HiddenInput, required=False)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('review', 'line_a', 'line_b', 'text')
