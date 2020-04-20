from django import forms
from home.models import News
from ckeditor import widgets
from django.utils.translation import ugettext as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)


class Newsform(forms.ModelForm):
    error_css_class = 'error'

    title = forms.CharField(label='', max_length=50, min_length=5, widget=forms.TextInput(attrs={
        'class':'form-element input-field',
        'placeholder':'Xəbər başlığı',
        'type':'text'
    }),required=True,error_messages={'invalid' : 'Bu xana bos ola bilmez','required' : 'Bu xana bos ola bilmez'})
    content = forms.CharField(label='',widget=widgets.CKEditorWidget(attrs={
        'class':'form-element input-field',
        'placeholder':'Xəbərin məzmunu'

    }),required=True)
    image = forms.FileField(label='',required=False,widget=forms.FileInput(attrs={'id' : 'choosefile','class':'file_upl',
    'type':'file',
    'name' : 'choosefile',
    
    }))
    class Meta:
        model = News
        fields = ['title','content','image',]
        
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')  
    #     if 'a' in title == False:
    #         raise forms.ValidationError('Xeber basligi bos ola bilmez')
    




class PublicationForm(forms.ModelForm):
    error_css_class = 'error'
    
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'text',
        'placeholder': 'Mənt'
    }))
    file = forms.FileField(label='', widget=forms.ClearableFileInput(attrs={
        'class': 'file'
    }))

class TaskForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput)
    description = forms.CharField(label="", widget=forms.TextInput)
    added_date = forms.DateField(label=,widget=forms.DateInput)
    deadline = forms.DateField(label="",widget=forms.DateInput)
    status = forms.BooleanField(label="")

