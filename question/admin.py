from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Question, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Comment Information', {"fields": ('author', 'parent', 'question', 'content',),}),
        )

    list_display = ('id', 'author', 'question', 'parent')
    list_filter = ['author', 'question__title']
    search_fields = ['author__username', 'question__title', 'id']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Question Information', {"fields": ('author', 'tags', 'title', 'slug', 'likes', 'like_count', 'content','date_posted'),}),
        )

    list_display = ( 'title','id', 'author')
    list_filter = ['tags', 'author']
    search_fields = ['id', 'slug']

    inlines = [CommentInLine]



