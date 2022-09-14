# from functools import cached_property
from re import template
from django.db import models


from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json

from wagtail.documents.models import Document, AbstractDocument


from wagtail.models import Page,Orderable
from wagtail.fields import RichTextField
from wagtail.core.fields import RichTextField
from wagtail.admin.panels import FieldPanel,InlinePanel

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtail.contrib.forms.models import (
    AbstractFormField,
    AbstractForm,
    AbstractFormSubmission,
)

from wagtail.search import index

from django.contrib.auth.models import User



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('author', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    # thepage = Key(FormPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

# class CustomDocument(AbstractDocument):
#     # Custom field example:
#     source = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True
#     )

#     admin_form_fields = Document.admin_form_fields + (
#         # Add all custom fields names to make them appear in the form:
#         'source',
#     )

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
    ]