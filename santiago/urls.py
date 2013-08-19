from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from santiago.views import purchase_chips, top_up_chips, tables_list, table_view, \
                            member_page, account_settings, issue_403, verify_phone, \
                            SignupView, GetStartedView, VerifyView, ActivationView, \
                            VerifyPhoneView, LiveAceLoginView, GetStartedFbView, UpgradeOfferView

urlpatterns = patterns("santiago.views",
    # Member Page
    url(r"^$", member_page, name="member_page"),
    url(r"^account_settings/$", account_settings, name="account_settings"),
    url(r"^auction/$", "member_auction", name="member_auction"),
    url(r"^referral/$", "member_referral", name="member_referral"),
    url(r"^partner/$", "member_partner", name="member_partner"),

    # Account / Signup stuff
    url(r"^signup/$", issue_403, name="url-override-403"),
    url(r"^signup/(?P<activation_key>\w+)/$", SignupView.as_view(), name="account_signup"),
    url(r"^login/$", LiveAceLoginView.as_view(), name="account_login"),
    url(r"^login-fb/$", "login_fb", name="account_login_fb"),
    url(r"^get-started/$", GetStartedView.as_view(), name="account_get_started"),
    url(r"^get-started-fb/$", GetStartedFbView.as_view(), name="account_get_started_fb"),
    url(r"^verify/$", VerifyView.as_view(), name="account_verify"),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name="account_activate"),
    url(r'^verify-phone/$', VerifyPhoneView.as_view(), name="verify-phone"),
    url(r'^upgrade-offer/$', UpgradeOfferView.as_view(), name="upgrade_offer"),

    url(r'^uname/$', "validate_username", name="validate_username"),
    url(r'^password/$', "validate_password", name="validate_password"),

    # Chips stuff
    url(r"^reload/$", purchase_chips, name="purchase-chips"),
    url(r"^billing/$", "chip_billing", name="chip-billing"),
    url(r"^do-purchase/$", "do_purchase", name="do-purchase"),
    url(r"^top-up/$", top_up_chips, name="top-up-chips"),
    url(r"^do-top-up/$", "perform_top_up", name="perform-top-up"),

    # Table / gameplay stuff
    url(r"^lobby/$", tables_list, name="tables-list"),
    url(r"^view/(?P<table_id>\d+)/$", table_view, name="table-view"),
)
