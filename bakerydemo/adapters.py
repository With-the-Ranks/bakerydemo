import os
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def _csv_set(name: str, default: str = "") -> set[str]:
    raw = os.getenv(name, default) or ""
    return {x.strip().lower() for x in raw.split(",") if x.strip()}


ALLOWED_DOMAINS = _csv_set("GOOGLE_ADMIN_ALLOWED_DOMAINS", "350.org")
SUPERUSER_EMAILS = _csv_set("GOOGLE_ADMIN_SUPERUSERS", "")
DEFAULT_GROUP = os.getenv("GOOGLE_ADMIN_DEFAULT_GROUP", "Editors")


class AdminGoogleAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = (sociallogin.user.email or "").strip().lower()
        if "@" not in email:
            raise PermissionDenied("Google did not provide an email address")

        domain = email.split("@", 1)[1]
        if domain not in ALLOWED_DOMAINS:
            raise PermissionDenied("Not allowed")

        sociallogin.user.is_staff = True

        # Only allowlisted emails become superusers
        sociallogin.user.is_superuser = (email in SUPERUSER_EMAILS)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        group, _ = Group.objects.get_or_create(name=DEFAULT_GROUP)
        user.groups.add(group)
        return user
