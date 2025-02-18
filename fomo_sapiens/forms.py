from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField
from django.contrib import messages

class CustomSignupForm(SignupForm):
    """
    Custom signup form that adds CAPTCHA validation and custom username handling.

    This form extends the allauth `SignupForm` and introduces a CAPTCHA field 
    to protect against bots. Additionally, the username field is customized 
    with a placeholder for better user experience.
    """
    username = forms.CharField(
        max_length=30, 
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    captcha = CaptchaField(required=True, label="Just a quick humanity check. No pressure!")
    
    
    def save(self, request):
        """
        Save the new user after performing any custom logic (if needed).
        
        This method overrides the parent `save` method to create a new user, 
        allowing for additional actions such as email verification, role assignment,
        or success messages. The new user instance is returned after these steps.
        
        Args:
            request: The HTTP request object that contains the user data.

        Returns:
            user: The created user instance.
        """
        user = super().save(request)
        messages.success(request, 'User created successfully.')
        return user
    
    
    def clean(self):
        """
        Custom validation to handle CAPTCHA errors and provide user feedback.

        This method extends the default validation to ensure that CAPTCHA is 
        completed successfully. If the CAPTCHA is invalid, a custom error message 
        is added to the form for user notification.
        
        Returns:
            cleaned_data: The cleaned data dictionary with any additional errors.
        """
        cleaned_data = super().clean()
        captcha = cleaned_data.get("captcha")

        if not captcha:
            # If CAPTCHA is invalid, add a custom error message to the form
            self.add_error('captcha', "Captcha verification failed. Please try again.")
        
        return cleaned_data