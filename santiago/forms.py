import hashlib
import random

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.safestring import mark_safe
from captcha.fields import CaptchaField

from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField

from santiago.models import UserProfile, SecurityQuestion, LEGAL_STATES, GENDER_CHOICES

import account.forms

class GetStartedForm(forms.Form):
    email = forms.EmailField(error_messages={'required': "Enter a valid email address"})
    captcha = CaptchaField(error_messages={'required': 'Invalid CAPTCHA'})

    def clean_email(self):
        # query user table for this email address
        qs = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not qs.exists():
            return self.cleaned_data["email"]
        raise forms.ValidationError("This email address was previously registered to \
                                        %s. If you have previously created an account, \
                                        click 'Login' above. If you forgot your password, \
                                        please reset your password by clicking 'Forgot \
                                        password?' on the Login page." % qs[0].username)

    @staticmethod
    def generate_activation_key(email):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        return hashlib.sha1(salt+email).hexdigest()


class VerifyForm(forms.Form):
    verification_code = forms.CharField();



def add_empty_choice(choices):
    choices = list(choices)
    choices.insert(0, (u"", u"---------"))
    return tuple(choices)



class SignupForm(account.forms.SignupForm):
    email = forms.EmailField(widget=forms.HiddenInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    street1 = forms.CharField(max_length=255)
    street2 = forms.CharField(required=False, max_length=255)
    city = forms.CharField(max_length=64)
    state = forms.ChoiceField(choices=add_empty_choice(LEGAL_STATES))
    zip = forms.CharField(max_length=64)
    security_question = forms.ModelChoiceField(SecurityQuestion.objects.all())
    security_answer = forms.CharField(max_length=50)
    phone = USPhoneNumberField()
    pin_delivery = forms.ChoiceField(widget=forms.RadioSelect, choices=UserProfile.PIN_DELIVERY_CHOICES)
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1994)))
    gender = forms.ChoiceField(choices=add_empty_choice(GENDER_CHOICES))
    email_policy = forms.BooleanField(help_text="I agree to LiveAce's <a href='#'>email policy</a>.")
    terms_and_conditions = forms.BooleanField(help_text="I agree to LiveAce's <a href='#'>Terms & Conditions</a>.")

    def clean_password(self):
        MIN_LENGTH = 6
        MAX_LENGTH = 25
        
        password = self.cleaned_data["password"]

        if len(password) < MIN_LENGTH or len(password) > MAX_LENGTH:
            raise forms.ValidationError("Your password must contain %d-%d characters." % (MIN_LENGTH, MAX_LENGTH))

        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError("Password must contain at least one letter and at least one digit.")

        return password

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        dupes = UserProfile.objects.filter(phone=phone)
        if dupes.count() > 0:
            username = dupes[0].user.username
            raise forms.ValidationError(mark_safe("The phone number %s was previously registered to username %s. If you have previously created an account, click 'Log In' above. If you forgot your passwrod, you can re-set it by clicking 'Forgot password' on the Login page. If you did not previously register an account under username %s, please <a href='#'>contact us</a> and we will be able to assist you with this process." % (phone, username, username)))
        return phone
