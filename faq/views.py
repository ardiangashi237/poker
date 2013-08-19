from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from faq.models import Faq, FaqCategory

def faq_general(request):
    cat = FaqCategory.objects.get(id=1)
    categories = FaqCategory.objects.all().order_by('sequence')
    faqs = Faq.objects.all().filter(category=cat).order_by('sequence')
    return render(request, "faq.html", {"faq_title": cat.title, "faq_category": cat.name, "faq_categories": categories, "faqs":faqs})
    #return render (request, "faq.html")

def faq_detail(request, category_slug):
    cat = FaqCategory.objects.get(slug=category_slug)
    categories = FaqCategory.objects.all().order_by('sequence')
    faqs = Faq.objects.all().filter(category=cat).order_by('sequence')
    return render(request, "faq.html", {"faq_title": cat.title, "faq_category": cat.name, "faq_categories": categories, "faqs":faqs})

