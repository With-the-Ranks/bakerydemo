import os
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

ALLOWED_DOMAINS = os.getenv("GOOGLE_ADMIN_ALLOWED_DOMAINS", set("350.org"))
SUPERUSER_EMAILS = os.getenv("GOOGLE_ADMIN_SUPERUSERS")
DEFAULT_GROUP = os.getenv("GOOGLE_ADMIN_DEFAULT_GROUP", "Editors")


class AdminGoogleAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = (sociallogin.user.email or "").lower()
        domain = email.split("@")[-1] if "@" in email else ""
        if domain not in ALLOWED_DOMAINS:
            raise PermissionDenied("Not allowed")

        sociallogin.user.is_staff = True

        # Only allowlisted emails become superusers
        if email in SUPERUSER_EMAILS:
            sociallogin.user.is_superuser = True

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        group, _ = Group.objects.get_or_create(name=DEFAULT_GROUP)
        user.groups.add(group)
        return user
