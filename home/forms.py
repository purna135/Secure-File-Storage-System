from django import forms
from .models import myuser
from django.core.validators import validate_email


class RegForm ( forms . ModelForm):
    Confirm_Password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Confirm Password'}
    ), required=True, max_length=20)

    class Meta:
        model = myuser
        fields = ['Username', 'Email', 'Password', 'Confirm_Password']
        widgets = {
            'Username': forms.TextInput(attrs={'class': 'form-control input-block', 'placeholder': 'Username'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control input-block', 'placeholder': 'Your Email'}),
            'Password': forms.PasswordInput(attrs={'class': 'form-control input-block', 'placeholder': 'Password'})
        }

    def clean_Username(self):
        user = self.cleaned_data['Username']
        try:
            match = myuser.objects.get(Username=user)
        except:
            return self.cleaned_data['Username']
        raise forms.ValidationError("Username already exist")

    def clean_Email(self):
        email = self.cleaned_data['Email']
        try:
            mt = validate_email(email)
        except:
            return forms.ValidationError("Incorrect email format")
        return email

    def clean_Confirm_Password(self):
        pass1 = self.cleaned_data['Password']
        pass2 = self.cleaned_data['Confirm_Password']
        if pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError("Two passwords not same")
            MAX_LEN = 8
            if len(pass1) < MAX_LEN:
                raise forms.ValidationError("Password should be %d characters" %MAX_LEN)
            if pass1.isdigit():
                raise forms.ValidationError("Password should not all numeric")

