from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import santiago.views

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^howtoplay/$", direct_to_template, {"template": "howtoplay.html"}, name="howTo"),
    url(r"^legal/$", direct_to_template, {"template": "legal.html"}, name="legal"),
    url(r"^membership/$", direct_to_template, {"template": "membership.html"}, name="membership"),
    url(r"^about/$", direct_to_template, {"template": "about.html"}, name="about"),
    url(r"^contact/$", direct_to_template, {"template": "contact.html"}, name="contact"),
    url(r"^press/$", direct_to_template, {"template": "press.html"}, name="press"),
    url(r"^privacy/$", direct_to_template, {"template": "privacy.html"}, name="privacy"),
    url(r"^terms/$", direct_to_template, {"template": "terms.html"}, name="terms"),
    url(r"^channel/$", direct_to_template, {"template": "channel.html"}, name="channel"),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/", include("santiago.urls")),
    url(r"^account/", include("account.urls")),
    url(r"^captcha/", include("captcha.urls")),

    url(r"^chips/", include("santiago.urls")),
    url(r"^faq/", include("faq.urls")),
    url(r"^tables/", include("santiago.urls")),
    url(r"^AVATAR/(?P<user_id>\d+)/$", santiago.views.get_avatar, name="get-avatar"),

    url(r"^admin/django-ses/", include('django_ses.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
