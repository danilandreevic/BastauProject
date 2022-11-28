from django.contrib import admin
from django.utils.safestring import mark_safe

from BastauApp.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("title",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "Fio", "Educational_institution", "age", "region", "Direction_of_study", "Education")
    list_display_links = ("user",)
    list_filter = ('Education', 'Direction_of_study')
    search_fields = ("Fio", "Educational_institution")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("user", "Fio", "name_of_partner", "get_avatar",)
    list_display_links = ("user",)
    list_filter = ('name_of_partner',)
    search_fields = ("Fio",)
    # readonly_fields = ("user", "get_avatar")
    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src={obj.avatar.url} width ="100" height ="110"')
        else:
            return mark_safe('-')

    get_avatar.short_description = "Аватар"


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0



@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("id","title", "date_of_create", "date_of_edit", "date_of_close", "category", "is_published","tags",)
    list_display_links = ("title",)
    list_filter = ('category','is_published')
    search_fields = ("title",)
    # readonly_fields = ("user_id",)

    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "id_student","id_case", "status")
    list_display_links = ("id_student",)
    list_filter = ('status',)
    search_fields = ("id_student__Fio",'id_case__title')
    # readonly_fields = ("id_student","id_case")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('email','phone','password')
    list_display = ("email", "phone")
    list_filter = ('is_student','is_partner')
    search_fields = ("email",)

admin.site.site_header = "Администрация BastauProject"

