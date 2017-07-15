from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    honeypot = forms.CharField(required=False,
                               label='If you enter anything in this field, you comment will be treated as spam!')
    class Meta:
        model = Comment
        fields = ('content', 'parent', 'post')

    # 验证honeypot字段，如果有输入，则是垃圾评论
    def clean_honeypot(self):
        value = self.cleaned_data['honeypot']
        if value:
            return forms.ValidationError(self.fields['honeypot'].error_message)
        return value