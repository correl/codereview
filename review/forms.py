from django import forms
from codereview.review.models import *

class NewCommitReviewForm(forms.Form):
    author = forms.IntegerField(widget=forms.HiddenInput)
    repo = forms.IntegerField(widget=forms.HiddenInput)
    ref = forms.CharField(widget=forms.HiddenInput)
