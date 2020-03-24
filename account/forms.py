from django import forms
from account.models import CustomUser



class RegisterForm(forms.ModelForm):
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
    phone_number = forms.CharField(label='', max_length=20, widget=forms.TextInput(attrs={
        'class' : "input",
        'placeholder': "Phone number"
    }))

    field_order =  ('email','first_name', 'last_name', 'password', 'confirm_password', 'phone_number')


    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name', 'password', 'phone_number')


    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            # raise forms.ValidationError(
            #     "Password and Confirm Password does not match"
            # )
            self.add_error('confirm_password', 'Password and Confirm Password does not match')