from django.db import models
from django.template.defaultfilters import slugify

class FaqCategory(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    sequence = models.SmallIntegerField(blank=True, null=True)
    slug = models.SlugField(default=slugify(name))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faq categories"


class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=512)
    category = models.ForeignKey(FaqCategory)
    sequence = models.SmallIntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.question
