from django.test import TestCase
from django.contrib.messages import get_messages
from fomo_sapiens.forms import CustomSignupForm


class CustomSignupFormTestCase(TestCase):

    def test_form_valid_data(self):
        form_data = {
            "username": "validuser",
            "password1": "validpassword123",
            "password2": "validpassword123",
            "captcha": "PASSED",
        }
        form = CustomSignupForm(data=form_data)

        self.assertTrue(form.is_valid())
        user = form.save(self.client)

        self.assertEqual(user.username, "validuser")
        storage = get_messages(self.client)
        messages_list = list(storage)
        self.assertEqual(str(messages_list[0]), "User created successfully.")

    def test_form_invalid_captcha(self):
        form_data = {
            "username": "validuser",
            "password1": "validpassword123",
            "password2": "validpassword123",
            "captcha": "",
        }
        form = CustomSignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("captcha", form.errors)
        self.assertEqual(
            form.errors["captcha"], ["Captcha verification failed. Please try again."]
        )

    def test_form_missing_username(self):
        form_data = {
            "username": "",
            "password1": "validpassword123",
            "password2": "validpassword123",
            "captcha": "PASSED",
        }
        form = CustomSignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertEqual(form.errors["username"], ["This field is required."])

    def test_form_password_mismatch(self):
        form_data = {
            "username": "validuser",
            "password1": "validpassword123",
            "password2": "mismatchpassword123",
            "captcha": "PASSED",
        }
        form = CustomSignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertEqual(
            form.errors["password2"], ["The two password fields didn’t match."]
        )

    def test_form_username_placeholder(self):
        form = CustomSignupForm()

        username_widget = form.fields["username"].widget
        self.assertEqual(username_widget.attrs["placeholder"], "Username")

    def test_save_method(self):
        form_data = {
            "username": "validuser",
            "password1": "validpassword123",
            "password2": "validpassword123",
            "captcha": "PASSED",
        }
        form = CustomSignupForm(data=form_data)
        form.is_valid()

        user = form.save(self.client)

        self.assertEqual(user.username, "validuser")
        storage = get_messages(self.client)
        messages_list = list(storage)
        self.assertEqual(str(messages_list[0]), "User created successfully.")
