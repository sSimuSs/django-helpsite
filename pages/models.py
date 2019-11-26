from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class HelpPages(MPTTModel):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True, null=True)
    parent_page = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta(object):
    #     ordering = ['position']

    class MPTTMeta:
        parent_attr = 'parent_page'
        # tree_id_attr = 'position'
        # order_insertion_by = ['position']

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(HelpPages, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
