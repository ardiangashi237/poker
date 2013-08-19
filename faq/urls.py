from django.conf.urls import patterns, include, url

urlpatterns = patterns("faq.views",
    url(r"^$", "faq_general", name="faq-general"),
    url(r"^(?P<category_slug>[\w-]+)/?$", "faq_detail", name="faq-detail"),
)

