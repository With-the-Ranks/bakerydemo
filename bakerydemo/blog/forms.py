from wagtail.admin.forms import WagtailAdminPageForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogPageForm(WagtailAdminPageForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("first_name", "last_name", "username"),
        required=False,
        label="Author",
        widget=forms.Select,  # force a simple dropdown
    )

    def __init__(self, *args, **kwargs):
        current_user = kwargs.get("for_user") or kwargs.get("user")
        super().__init__(*args, **kwargs)

        self.fields["author"].label_from_instance = (
            lambda u: u.get_full_name() or u.email or u.get_username()
        )

        if current_user and getattr(current_user, "is_authenticated", False):
            field = self.fields["author"]
            bound_name = self.add_prefix("author")

            if self.is_bound and not self.data.get(bound_name):
                data = self.data.copy()
                data[bound_name] = str(current_user.pk)
                self.data = data
            else:
                field.initial = current_user.pk
                self.initial.setdefault("author", current_user.pk)
