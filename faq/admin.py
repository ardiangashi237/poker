from django.contrib import admin
from faq.models import FaqCategory, Faq
from django import forms

class FaqForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Faq

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'sequence',)
    list_editable = ('sequence',)
    list_display_links = ('question',) 
    form = FaqForm
admin.site.register(FaqCategory)
admin.site.register(Faq, FaqAdmin)
