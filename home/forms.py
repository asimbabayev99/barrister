from django import forms
from home.models import News
from ckeditor import widgets


class Newsform(forms.ModelForm):
    error_css_class = 'error'
    title = forms.CharField(label='',max_length=50,min_length=10,widget=forms.TextInput(attrs={'class':'input','placeholder':'Basliq'}))
    content = forms.CharField(label='',widget=widgets.CKEditorWidget(attrs={'class':'input'}))
    image = forms.ImageField(label='',required=False)


    class Meta:
        model = News
        fields = ['title','content','image',]


