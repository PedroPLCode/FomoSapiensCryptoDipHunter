from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Signals",
            {
                "fields": (
                    "email_signals_receiver",
                    "email_gpt_analysis_receiver",
                    "telegram_signals_receiver",
                    "telegram_gpt_analysis_receiver",
                    "telegram_chat_id",
                )
            },
        ),
    )


admin.site.register(UserProfile, UserProfileAdmin)
