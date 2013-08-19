from django.core.urlresolvers import reverse_lazy
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.conf import settings
from django.contrib import messages

from django.contrib.auth.models import User

from models import UserProfile, ChipPackage, RegistrationProfile, RegistrationProfileVerification, PokerTable, PokernetUser, PokernetChipCount, UserChipCount, MembershipLevel, Avatar, Badge

import account.views
from account.forms import alnum_re
from forms import SignupForm, GetStartedForm, VerifyForm

def issue_403(request):
    return HttpResponseForbidden("access is forbidden")

@login_required
def member_page(request):
    user = request.user
    badges = Badge.objects.all().order_by('sequence') 
    ctx = { "user" : user, "badges" : badges }
    return render(request, "member_page.html", ctx)

def account_settings(request):
    user = request.user
    avatars = Avatar.objects.all()
    ctx = {"user": user, "avatars":avatars }
    return render(request, "member_settings.html", ctx)

def member_auction(request):
    user = request.user
    ctx = {"user": user }
    return render(request, "member_auction.html", ctx)

def member_referral(request):
    user = request.user
    ctx = {"user": user }
    return render(request, "member_referral.html", ctx)

def member_partner(request):
    user = request.user
    ctx = {"user": user }
    return render(request, "member_partner.html", ctx)

class VerifyPhoneView(TemplateView):
    template_name = "account/verify_phone.html"
    
    def post(self, *args, **kwargs):
        pin = self.request.POST["pin"]
        if pin == "1111":
            return redirect("upgrade_offer")
            #return redirect("account_login")
        else:
            return render(self.request, self.template_name)

class UpgradeOfferView(TemplateView):
    template_name = "upgrade_offer.html"

    def post(self, request, *args, **kwargs):
        user = request.session["current_user"].get_profile()
        # upgrade user to premium or leave in premium-trial state
        action = request.POST['action']

        if action == "upgrade_now":
            user.upgrade_to_premium()

        return redirect("account_login")


def verify_phone(request):
    return render(request, "account/verify_phone.html")


@login_required
def purchase_chips(request):
    user = request.user.get_profile()
    
    if not user.current_member_level.allow_chip_purchases:
        messages.info(request, "Sorry, %s Players cannot purchase chips." % 
                        user.current_member_level.name)
        return redirect("member_page")

    chips_this_week = user.chips_this_week()
    weekly_max = settings.WEEKLY_CHIP_MAX

    packages = ChipPackage.objects.all()
    ctx = { 'packages': packages, 'chips_this_week': chips_this_week, 'weekly_max': weekly_max }
    return render(request, 'purchase_chips.html', ctx)


@login_required
@require_POST
def do_purchase(request):
    try:
        chip_package_id = request.POST['chip_package_id']
        request.user.get_profile().purchase_chip_package(chip_package_id)
        messages.info(request, "Your chips have been purchased!")
    except:
        raise
        messages.info(request, "There has been a problem buying this chip package.")

    return redirect("member_page")


@login_required
def chip_billing(request):
    chip_package_id = request.POST['chip_package_id']
    pkg = ChipPackage.objects.get(id=chip_package_id)

    ctx = {'package': pkg}

    return render(request, 'billing.html', ctx)


@login_required
def top_up_chips(request):
    user = request.user.get_profile()

    if user.at_table():
        messages.info(request, "You must leave all game tables before attempting to top up.")
        return redirect("member_page")

    daily_threshold = user.current_member_level.daily_top_up_threshold 
    user_chips = user.user_real_chip_balance()
    if daily_threshold <= user_chips:
        messages.info(
                request, 
                "Since you have %d chips, you are not eligible to top up to %d chips." % 
                    (user_chips, daily_threshold)
        )
        return redirect("member_page")

    if user.topped_up_today():
        messages.info(request, "Sorry, but you have already topped up today.")
        return redirect("member_page")

    return render(request, 'chips/daily_top_up.html')


@login_required
@require_POST
def perform_top_up(request):
    try:
        request.user.get_profile().perform_top_up()
        messages.info(request, "You've been topped up!")
    except:
        messages.info(request, "There has been a problem topping you up.")

    return redirect("member_page")


class VerifyView(FormView):
    template_name = "verify.html"
    form_class = VerifyForm
    success_url = reverse_lazy("account_signup")


class ActivationView(View):
    def get(self, request, *args, **kwargs):
        key = kwargs['activation_key']

        try:
            reg_pro = RegistrationProfile.objects.get(activation_key=key)
        except RegistrationProfile.DoesNotExist:
            return HttpResponse("unknown activation key")

        if not hasattr(reg_pro, "verification"): # using verification link for first time
            verify = RegistrationProfileVerification(
                            registration_profile = reg_pro,
                            client_ip = request.META["REMOTE_ADDR"],
                            client_host = request.META["REMOTE_HOST"],
            )
            verify.save()

        return redirect("account_signup", key)

class GetStartedFbView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        fb_id = request.POST["fb_id"]
        activation_key = GetStartedForm.generate_activation_key(email)
        reg_pro = RegistrationProfile(
                        email = email,
                        facebook_id = fb_id,
                        client_ip = request.META["REMOTE_ADDR"],
                        client_host = request.META["REMOTE_HOST"],
                        activation_key = activation_key,
                        joined_via_fb = True
        )
        reg_pro.save()
        return redirect("account_activate", activation_key=activation_key)
    


class GetStartedView(FormView):
    template_name = 'get_started.html'
    form_class = GetStartedForm
    success_url = reverse_lazy("account_verify")

    def get_context_data(self, **kwargs):
        ctx = super(GetStartedView, self).get_context_data(**kwargs)
        ctx.update({
            "facebook_app_id": settings.FACEBOOK_APP_ID
        })
        return ctx

    def form_valid(self, form):
        email = form.cleaned_data['email']
        activation_key = form.generate_activation_key(email)
        reg_pro = RegistrationProfile(
                        email = email,
                        client_ip = self.request.META["REMOTE_ADDR"],
                        client_host = self.request.META["REMOTE_HOST"],
                        activation_key = activation_key,
        )
        reg_pro.save()

        act_link = self.request.build_absolute_uri("/account/activate/%s" % activation_key)

        if settings.DEBUG:
            messages.info(self.request, "Email sent to %s with link %s" % (email, act_link))
            
        self.send_confirmation(email, activation_key, act_link)
        return super(FormView, self).form_valid(form)

    def send_confirmation(self, email, activation_key, activation_link):
        ctx = {
            "user": email,
            "activate_url": activation_link,
	        "current_site": "",
            "key": activation_key,
        }
        subject = render_to_string("account/email/email_confirmation_subject.txt", ctx)
        subject = "".join(subject.splitlines()) # remove superfluous line breaks
        message = render_to_string("account/email/email_confirmation_message.txt", ctx)
        send_mail(subject, message, "admin@liveace.com", [email])

class LiveAceLoginView(account.views.LoginView):
    def get_context_data(self, **kwargs):
        ctx = super(LiveAceLoginView, self).get_context_data(**kwargs)
        ctx.update({
            "facebook_app_id": settings.FACEBOOK_APP_ID
        })
        return ctx

@require_POST
def login_fb(request):
    fb_id = request.POST["fb_id"]
    try:
        profile = UserProfile.objects.get(facebook_id=fb_id)
        # set backend on User object to bypass needing to call auth.authenticate
        #profile.user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(request, profile.user)
        return redirect("member_page")
    except UserProfile.DoesNotExist:
        messages.info(request, "Sorry, your facebook account hasn't been registered with LiveAce. Please use your LiveAce credentials to login.")
        return redirect("account_login")


def validate_username(request):
    username = request.GET['uname']

    if not alnum_re.search(username):
        return HttpResponse(False)

    qs = User.objects.filter(username__iexact=username)
    if not qs.exists():
        return HttpResponse(True)
    return HttpResponse(False)


def validate_password(request):
    # when changing this method, be sure to see also santiago.forms.SignupForm.clean_password
    MIN_LENGTH = 6
    MAX_LENGTH = 25

    p = request.GET['pass']

    if len(p) < MIN_LENGTH or len(p) > MAX_LENGTH:
        return HttpResponse(False)

    first_isalpha = p[0].isalpha()
    if all(c.isalpha() == first_isalpha for c in p):
        return HttpResponse(False)

    return HttpResponse(True)

class SignupView(account.views.SignupView):

    form_class = SignupForm

    def get(self, *args, **kwargs):
        key = kwargs['activation_key']
        try:
            reg_pro = RegistrationProfile.objects.get(activation_key=key)

            if not reg_pro.verification:
                return HttpResponse("How did you get here? Verify your email first!")

        except RegistrationProfile.DoesNotExist:
            return HttpResponse("unknown activation key")
        return super(SignupView, self).get(*args, **kwargs)
        

    def after_signup(self, user, form):
        self.create_profile(form, user)
        super(SignupView, self).after_signup(user, form)

    def create_user(self, form, commit=True, **kwargs):
        user = super(SignupView, self).create_user(form, commit, **kwargs)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def login_user(self, user):
        # overriding this method so the user actually does not get logged in
        # also remove the "logged_in" message so we don't lie to the user
        self.messages.pop("logged_in", "nevermind")

        # however let's save the user in the session so that we can 
        #   know who this is from now till he logs in
        self.request.session["current_user"] = user


    def create_profile(self, form, user):
        activation_key = self.kwargs['activation_key']
        reg_pro = RegistrationProfile.objects.get(activation_key=activation_key)
        fb_id = reg_pro.facebook_id

        profile = UserProfile(user=user)
        profile.facebook_id = fb_id
        profile.street1 = form.cleaned_data["street1"]
        profile.street2 = form.cleaned_data["street2"]
        profile.city = form.cleaned_data["city"]
        profile.state = form.cleaned_data["state"]
        profile.zip = form.cleaned_data["zip"]
        profile.security_question = form.cleaned_data["security_question"]
        profile.security_answer = form.cleaned_data["security_answer"]
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.phone = form.cleaned_data["phone"]
        profile.pin_delivery = form.cleaned_data["pin_delivery"]
        profile.current_member_level = MembershipLevel.objects.get(pk=1) #freemium
        profile.save()

        # now do some pokernet / chip stuff, as a stop-gap till I get chip purchasing working
        pnet_user = PokernetUser(created=0, name=user.username, email=user.email, password="NOTUSED", affiliate=0, privilege=1, rating=1000, future_rating=1000, games_count=0)
        pnet_user.save()

        # hack to get newly saved instance so we know id/serial
        #   really don't understand why this isn't working
        pnet_user = PokernetUser.objects.get(name=pnet_user.name)

        pnet_chips = PokernetChipCount(user_serial = pnet_user.serial, currency_serial=1, amount=2000000, rake=0, points=0)
        pnet_chips.save()

        user_chips = UserChipCount(user=user, serial=pnet_user.serial, real_chips=200, live_chips=0, bank_chips=0)
        user_chips.save()
        


    def get_context_data(self, **kwargs):
        context =  super(SignupView, self).get_context_data(**kwargs)
        activation_key = self.kwargs['activation_key']
        reg_pro = RegistrationProfile.objects.get(activation_key=activation_key)
        context.update({
            'facebook_app_id': settings.FACEBOOK_APP_ID, 
            'activation_key': activation_key, 
            'email': reg_pro.email, 
            'is_fb': reg_pro.joined_via_fb
        })
        return context

    def get_success_url(self, fallback_url=None, **kwargs):
        return reverse_lazy("verify-phone")



@login_required
def tables_list(request):
    #selected_filter = request.matchdict.get('filter', 'all')
    selected_filter = "all"

    filter_hash = {
        "all" : "All",
        "no_limit_holdem" : "No Limit Holdem",
        "omaha" : "Omaha",
        "limit_holdem" : "Limit Holdem",
    }

    poker_tables = PokerTable.objects.all()

    ctx =  {
        'selected_filter' : selected_filter,
        'filter_hash' : filter_hash,
        'result_tables' : poker_tables,
    }
    
    return render(request, "tables/list.html", ctx)


@login_required
def table_view(request, table_id):
    auth_id = request.user.userchipcount.serial
    auth = csrf(request)
    csrf_token = str(auth["csrf_token"])
    table = { 'serial' : table_id }

    import memcache
    mc = memcache.Client(["127.0.0.1:11211"])
    mc.set(csrf_token, auth_id)

    ctx = {
            'endpoint' : settings.POKERD_URL,
            'auth' : csrf_token,
            'table' : table,
            'authenticated_userid' : auth_id,
    }
    return render(request, "tables/view.html", ctx)


def get_avatar(request, user_id):
    return HttpResponseRedirect("%scss/images/profile-icon.png" % settings.STATIC_URL)
