from .models import (Post, Comments)
from django import forms


class PostForm(forms.ModelForm):
    """A ModelForm for posts."""

    class Meta:
        model   = Post
        fields  = ('message', )
        widgets = { 'message': forms.Textarea(attrs={'placeholder': 'Add Post',
                                                        'style': 'height: 70vh'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label = 'Post: '


class CommentForm(forms.ModelForm):
    """A ModelForm for Comments."""

    class Meta:
        model = Comments
        fields = ('text',)
        widgets = { 'text': forms.Textarea(attrs={'placeholder': 'Add comment'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Comment: '
        # self.fields['text'].placeholder = 'Comment: '