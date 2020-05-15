from django import forms
from .models import CustomUser, SERIYA_TYPES, PHONE_PREFIXES, Role, JobCategory
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from .models import PHONE_PREFIXES, GENDER_CHOICES



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





class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
    }
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password    


class UserUpdateForm(forms.ModelForm):
    error_css_class = 'error'
  
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Ad"
    })) 
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'class' : "form-element input-field",
        'placeholder': "Soyad"
    })) 
    middle_name = forms.CharField(label='', max_length=32, required=False, widget=forms.TextInput(attrs={
        'class': 'form-element input-field',
        'placeholder': 'Ata adı'
    }))
    address = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Adress'
    }))
    fin = forms.CharField(label='', max_length=10, required=False, widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': "Fin"
    }))
    seriya_type = forms.ChoiceField(choices=SERIYA_TYPES, required=False, widget=forms.Select(attrs={
        'class': 'custom-select'
    }))
    seriya = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Seriya'
    }))
    phone_prefix = forms.ChoiceField(choices=PHONE_PREFIXES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    phone_number = forms.IntegerField(required= True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'type' : 'text',
        'placeholder': 'Phone Number'
    }))

    field_order =  ('first_name', 'last_name', 'middle_name', 'address', 'fin', 'seriya_type', 'seriya', 'phone_number')


    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'middle_name', 'address', 'fin', 'seriya_type', 'seriya', 'phone_number')





class ProfileUpdateForm(forms.ModelForm):
    error_css_class = 'error'

    image = forms.ImageField(required=False)
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
    }))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control'
    }))
    address = forms.CharField(max_length=256, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address'
    }))

    # social networks
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
    }))
    twitter_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
    }))
    linkedin_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
    }))
    google_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
    }))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    work_summary = forms.CharField(max_length=2014, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    biography = forms.CharField(max_length=2014, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    job_category = forms.ModelChoiceField(required=False, queryset=JobCategory.objects.all(), widget=forms.Select(attrs={
        'class': 'form-element input-field',
    }))  
