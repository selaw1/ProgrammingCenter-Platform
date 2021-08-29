from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Language, DataStructure


class DataStructureInLine(admin.TabularInline):
    model = DataStructure
    extra = 0


@admin.register(DataStructure)
class DataStructureAdmin(admin.ModelAdmin):

    fieldsets = (
        ('DataStructure Information', {"fields": ('name', 'slug', 'language', 'detail'),}),
        )

    prepopulated_fields = {'slug':['name']}
    list_display = ('id', 'name', 'language')
    list_filter = ['language']
    search_fields = ['name', 'language__name', 'id']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Language Information', {"fields": ('name', 'slug', 'category', 'detail'),}),
        )

    prepopulated_fields = {'slug':['name']}
    list_display = ('name', 'id',)
    list_filter = ['category']
    search_fields = ['name', 'id']

    inlines = [DataStructureInLine]



@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title','related_languages_count', 'related_languages_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':['name']}
    list_filter = ['parent']
    search_fields = ['name','id']


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative language count
        qs = Category.objects.add_related_count(
                qs,
                Language,
                'category',
                'languages_cumulative_count',
                cumulative=True)

        # Add non cumulative language count
        qs = Category.objects.add_related_count(qs,
                 Language,
                 'category',
                 'languages_count',
                 cumulative=False)
        return qs

    def related_languages_count(self, instance):
        return instance.languages_count
    related_languages_count.short_description = 'Related languages (for this specific category)'

    def related_languages_cumulative_count(self, instance):
        return instance.languages_cumulative_count
    related_languages_cumulative_count.short_description = 'Related lanuages (in tree)'
