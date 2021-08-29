from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from ckeditor.fields import RichTextField

from programmingLanguage.models import Category
from account.models import UserBase



class Question(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    content = RichTextField(null=False, blank=False)
    tags = TreeManyToManyField(Category, related_name='cat_questions')
    author = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='questions')
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(UserBase, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    class Meta:
        ordering = ['-date_posted']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def  get_absolute_url(self):
        return reverse('question:question_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

class Comment(MPTTModel):
    author = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    publish_date = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['publish_date']

    def __str__(self):
        return self.content

