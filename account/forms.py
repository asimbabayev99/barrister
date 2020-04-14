from django import forms
from .models import CustomUser, SERIYA_TYPES, PHONE_PREFIXES, Role



class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='', max_length=256, widget=forms.TextInput(attrs={
        'class' : 'input',
        'placeholder':"Email"
    }))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "input",
        'placeholder': "Password"
    })) 
    field_order = ('email', 'password')

    class Meta:
        model = CustomUser
        fields = ('email', 'password')




class RegisterForm(forms.ModelForm):
    error_css_class = 'error'
    email = forms.EmailField(label='', max_length=32, widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder':"Email"
    }))
    first_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "First Name"
    })) 
    last_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Last Name"
    })) 
    middle_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Middle Name'
    }))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "form-control",
        'placeholder': "Password"
    })) 
    confirm_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "form-control",
        'placeholder': "Confirm Password"
    })) 
    address = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Adress'
    }))
    fin = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Fin"
    }))
    seriya_type = forms.ChoiceField(choices=SERIYA_TYPES, required=True, widget=forms.Select(attrs={
        'class': 'custom-select'
    }))
    seriya = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Seriya'
    }))
    phone_prefix = forms.ChoiceField(choices=PHONE_PREFIXES, required=True, widget=forms.Select(attrs={
        'class': 'custom-select'
    }))
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'type' : 'text',
        'placeholder': 'Phone Number'
    }))

    # field_order =  ('email','first_name', 'last_name', 'middle_name', 'password', 'confirm_password')


    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name', 'middle_name', 'address', 'fin', 'seriya_type', 'seriya', 'phone_prefix', 'phone_number', 'password')

    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Password and Confirm Password does not match')




class UserForm(forms.ModelForm):
    error_css_class = 'error'
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : 'form-element input-field',
        'placeholder':"Email"
    }))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Ad"
    })) 
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Soyad"
    })) 
    middle_name = forms.CharField(label='', max_length=32, widget=forms.TextInput(attrs={
        'class': 'form-element input-field',
        'placeholder': 'Ata adı'
    }))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Şəfrə"
    })) 
    confirm_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Şifrəni təkrarla"
    })) 
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={
        'class': 'form-element input-field',
    }))
    image =  forms.ImageField()

    field_order =  ('email','first_name', 'last_name', 'middle_name', 'password', 'confirm_password', 'role')


    class Meta:
        model = CustomUser
        fields =  ('email','first_name', 'last_name', 'middle_name', 'password', 'confirm_password', 'role')


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Password and Confirm Password does not match')