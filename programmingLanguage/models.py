from django.db import models
from django.shortcuts import reverse

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from ckeditor.fields import RichTextField


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True)
    detail = RichTextField(blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('pl:category_detail', kwargs={'path': self.get_path()})

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    category = TreeManyToManyField(Category, related_name='lang_category')
    detail = RichTextField(blank=True, null=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class DataStructure(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='datastructure')
    detail = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
