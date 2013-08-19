# inputs: username, password, membership level
# membership levels are amoe, premium, freemium, freemium with trial

# I don't think I care about registration / registration verification
import string
import random

import argparse
import santiago.views
import santiago.forms

from santiago.models import SecurityQuestion

parser = argparse.ArgumentParser(description="Create a user with ease.")
parser.add_argument('username')
parser.add_argument('password')

args = parser.parse_args()


username = args.username
password = args.password

form_data = {
        "username" : username,
        "password" : password,
        "password_confirm" : password,
        "email" : "%s@autogen.com" % username,
        "first_name" : username,
        "last_name" : "User",
        "street1" : "%s Street" % username,
        "city" : "%sville" % username,
        "state" : "IL",
        "zip" : "61525",
        "security_question" : 1,
        "security_answer" : username,
        "phone" : string.join( [random.choice(string.digits) for i in range(10)], ""),
        "pin_delivery" : "TXT",
        "birthdate" : "1900-01-01",
        "gender" : "F",
        "email_policy" : True,
        "terms_and_conditions" : True
}

form = santiago.forms.SignupForm(form_data)
if form.is_valid():
    print "ready to create user"
    signup_view = santiago.views.SignupView()
    user = signup_view.create_user(form)
    signup_view.create_profile(form, user)

else:
    print form.errors

