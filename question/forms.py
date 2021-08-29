from django import forms
from django.template.defaultfilters import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from mptt.forms import TreeNodeChoiceField

from .models import Question, Comment
from programmingLanguage.models import Category


class QuestionCraetionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        help_texts = {'tags': "Hold down “Control”, or “Command” on a Mac, to select more than one."}

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        slug = slugify(title)

        if title and Question.objects.filter(slug=slug).exists():
            self.add_error('title', 'Question with this title already exists.')
        return cleaned_data
    
class QuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        help_texts = {'tags': "Hold down “Control”, or “Command” on a Mac, to select more than one."}

class QuestionSearchForm(forms.Form):
    query = forms.CharField()
    username = forms.CharField()
    tags = forms.ModelChoiceField(queryset=Category.objects.all())

    query.label = 'Question Title'
    tags.label = 'Question Tags'
    username.label = 'Question Author'

    tags.required = False
    username.required = False

    username.help_text = "Case Sensitive!"

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields['query'].widget.attrs.update({'placeholder':'Type Question title'})
        self.fields['username'].widget.attrs.update({ 'placeholder':'Type author username'})

        self.helper = FormHelper()
        self.helper.label_class = 'mt-3'



class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'question', 'parent']
        labels ={'content':''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields['content'].widget.attrs.update({'placeholder':'Comment here', 'class':'text form-control'})
        self.fields['parent'].widget.attrs.update({'class':'d-none'})
        self.fields['parent'].required = False
        self.fields['parent'].label = ''

    # def save(self, *args, **kwargs):
    #     Comment.objects.rebuild()
    #     return super(CommentCreateForm, self).save(*args, **kwargs)
