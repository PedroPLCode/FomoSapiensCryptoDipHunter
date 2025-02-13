from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField
from django.contrib import messages

class CustomSignupForm(SignupForm):
    """
    Custom signup form that adds a CAPTCHA field and custom username validation.

    The form extends the allauth SignupForm and includes a CAPTCHA field 
    for additional bot protection. The username field is also customized with 
    a placeholder.
    """
    username = forms.CharField(
        max_length=30, 
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    captcha = CaptchaField(required=True, label="Are you a human?")
    
    
    def save(self, request):
        """
        Save the new user after performing additional logic (if needed).
        
        This method calls the parent save method to create the user and then
        allows you to add extra logic (e.g., email verification, role assignment, etc.)
        before returning the user object.
        
        Args:
            request: The HTTP request object.

        Returns:
            user: The created user instance.
        """
        user = super().save(request)
        messages.success(request, 'User creadet succesfully')
        return user
    

    def clean(self):
        """
        Custom validation to handle CAPTCHA errors and add custom messages.
        """
        cleaned_data = super().clean()
        captcha = cleaned_data.get("captcha")

        if not captcha:
            # If CAPTCHA is invalid, add custom error message to form
            self.add_error('captcha', "Captcha verification failed. Please try again.")
        
        return cleaned_data