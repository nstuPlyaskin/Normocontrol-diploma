from django.contrib import admin

from .models import CheckOut, Remark


class CheckAdmin(admin.ModelAdmin):
    list_display = ('pk', 'student', 'docx_file', 'check_date',)
    search_fields = ('student',)
    list_filter = ('student',)
    empty_value_display = "-пусто-"


class RemarkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'check_date',)
    search_fields = ('text',)
    list_filter = ('text',)
    empty_value_display = "-пусто-"


admin.site.register(CheckOut, CheckAdmin)
admin.site.register(Remark, RemarkAdmin)
