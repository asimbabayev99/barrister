from django import forms
from account.models import CustomUser



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
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : 'input',
        'placeholder':"Email"
    }))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "input",
        'placeholder': "First Name"
    })) 
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "input",
        'placeholder': "Last Name"
    })) 
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "input",
        'placeholder': "Password"
    })) 
    confirm_password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'class' : "input",
        'placeholder': "Confirm Password"
    })) 
    field_order =  ('email','first_name', 'last_name', 'password', 'confirm_password')


    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name', 'password')


    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Password and Confirm Password does not match')