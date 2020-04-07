from django import forms
from home.models import News
from ckeditor import widgets


class Newsform(forms.ModelForm):
    error_css_class = 'error'
    title = forms.CharField(label='',max_length=50,min_length=5,widget=forms.TextInput(attrs={'class':'form-group form-control news-header','placeholder':'Xəbər başlığı'}))
    content = forms.CharField(label='',widget=widgets.CKEditorWidget(attrs={'class':'form-group form-control'}))
    image = forms.ImageField(label='',required=False,)


    class Meta:
        model = News
        fields = ['title','content','image',]


