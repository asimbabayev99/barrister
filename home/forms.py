from django import forms
from home.models import News
from ckeditor import widgets


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
    image = forms.FileField(label='',required=False,widget=forms.FileInput(attrs={'id' : 'choosefile',
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
