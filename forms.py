from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CustomLoginForm(LoginForm):
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'theme': 'light'}))

class CustomSignupForm(SignupForm):
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'theme': 'light'}))
