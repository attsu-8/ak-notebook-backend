from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models


# Userモデルをオーバーライドしたため、Adminの編集も必要
class UserAdmin(BaseUserAdmin):
    ordering = ["user_id"]
    list_display = ["user_email"]
    fieldsets = (
        (None, {"fields": ("user_email", "password")}),
        (_("Personal Info"), {"fields": ()}),
        (
            _("permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (None, {"classes": ("wide",), "fields": {"user_email", "password1", "password2"}})


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Note)
admin.site.register(models.MemoCategory)
admin.site.register(models.Purpose)
admin.site.register(models.Memo)
admin.site.register(models.StickyNoteCategory)
admin.site.register(models.StickyNote)
admin.site.register(models.BrowsingMemoCount)
admin.site.register(models.DmBrowsingMemoCount)
admin.site.register(models.DmLearningEfficiency)
admin.site.register(models.DmLearningEfficiencyBatchLog)
