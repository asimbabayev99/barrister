from django import forms
from home.models import News, Publication, Task, TASK_STATUS, Appointment, City , Contact
# from ckeditor import widgets
import ckeditor
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
    content = forms.CharField(label='',widget=ckeditor.widgets.CKEditorWidget(attrs={
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
    
    text = forms.CharField(label='', widget=ckeditor.widgets.CKEditorWidget(attrs={
        'class': 'text',
        'placeholder': 'Mənt'
    }))
    file = forms.FileField(label='', widget=forms.ClearableFileInput(attrs={
        'class': 'file file_upl bordered_upl'
    }))
    class Meta:
        model = Publication
        fields = ['text','file']



class TaskForm(forms.ModelForm):
    type = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={
        'class': 'form-element input-field',
        'placeholder': 'Tapşırıgın növü'
    }))
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-element input-field',
        'placeholder': 'Başlıq',
        'autocomplete': 'off'
    }))
    description = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={
        # 'class': 'form-element input-field',
        'placeholder': 'Tapşırığın qısa məzmunu',
        'cols': '50', 
        'rows': '3',
    }))
    media_file = forms.FileField(label="", required=False, widget=forms.FileInput(attrs={
        'name':'media_file',
        'id': 'chooseFile',
    }))
    due_date = forms.DateField(label="",widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    due_time = forms.TimeField(label="", required=False, widget=forms.TimeInput(attrs={
        'type': 'time',
        'style': 'margin-left: auto;',
        'class': 'that4 browser-default custom-select',
    }))
    # status = forms.ChoiceField(label="", choices=TASK_STATUS)

    class Meta:
        model = Task
        fields = ['type', 'title', 'description', 'media_file', 'due_date', 'due_time']




class AppointmentForm(forms.ModelForm):
    error_css_class = 'error'
    email = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder':"Email"
    }))
    first_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Ad"
    })) 
    last_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Soyad"
    })) 
    middle_name = forms.CharField(label='', max_length=32, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ata adı'
    }))
    phone = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'type' : 'text',
        'placeholder': 'Telefon'
    }))
    date = forms.DateField(
        # input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'data-target': '#datetimepicker1'
        })
    )
    time = forms.TimeField(
        # input_formats=['%H:%M'],
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    city = forms.ModelChoiceField(required=False, queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    zip = forms.CharField(label='', max_length=8, required=False, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Zip code"
    }))
    detail = forms.CharField(label='', max_length=256, required=False, widget=forms.Textarea(attrs={
        'class' : "form-control",
        'placeholder': "Görüşün detalları"
    }))

    class Meta:
        model = Appointment
        fields = ('email','first_name', 'last_name', 'middle_name', 'phone', 'date', 'time', 'city', 'zip', 'detail')
    
    
class ContactForm(forms.ModelForm):
    first_name = forms.CharField(label="",max_length=40,widget=forms.TextInput(attrs={'placeholder':'Ad'}))
    last_name = forms.CharField(label='' , max_length=40,widget=forms.TextInput(attrs={'placeholder':'Soyad'}),required = False)
    phone = forms.CharField(label='', max_length=20,widget=forms.TextInput(attrs={'placeholder':'Nomre'}),required=True)
    phone2 = forms.CharField(label='',max_length=20,required=False,widget=forms.TextInput(attrs={'placeholder':'Nomre2'}))
    email = forms.CharField(label='',max_length=20,required=False,widget=forms.TextInput(attrs={'placeholder':'Emaili'}))
    adress = forms.CharField(label='',max_length=20,required = False,widget=forms.TextInput(attrs={'placeholder':'Adress'}))

    class Meta:
        model = Contact
        fields = ['first_name','last_name','phone','phone2','email','adress']


