from django.contrib import admin
from pages.models import HelpPages
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from mptt.admin import MPTTModelAdmin , DraggableMPTTAdmin

# Register your models here.
class ChildPagesInline(admin.TabularInline):
    model = HelpPages
    extra = 0


class HelpPagesAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'page_title', 'slug', 'updated', 'date', 'status']
    # list_display = ('tree_actions', 'something')
    list_display_links = ('page_title',)

    def page_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,  # Or whatever you want to put here
        )
    # something.short_description = _('something nice')
    # ordering = ['position']
    search_fields = ['title', 'slug', 'id']
    list_editable = ['status',]
    # list_display_links = ['title']
    list_filter = ['status']
    list_per_page = 10
    inlines = [ChildPagesInline]


admin.site.register(HelpPages, HelpPagesAdmin)