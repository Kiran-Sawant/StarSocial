from .models import Comments
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        widgets = { 'text': forms.Textarea(attrs={'placeholder': 'Add comment'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Comment: '
        # self.fields['text'].placeholder = 'Comment: '