from django import forms
from allauth.account.forms import LoginForm, SignupForm
#from captcha.fields import ReCaptchaField
#from captcha.widgets import ReCaptchaV2Checkbox

#class CustomLoginForm(LoginForm):
    #recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'theme': 'light'}))
    

class CustomSignupForm(SignupForm):
    username = forms.CharField(
        max_length=30, 
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    #recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'theme': 'light'}))
    
    def save(self, request):
        user = super().save(request)
        # Możesz dodać dodatkową logikę, jeśli potrzebujesz
        return user
