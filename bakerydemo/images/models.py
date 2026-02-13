from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    credit = models.CharField(max_length=255, blank=True)
    description = models.TextField(
        blank=True,
        help_text="Editorial description or notes about the image",
    )

    admin_form_fields = Image.admin_form_fields + (
        "description",
        "credit",
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("image", "filter_spec", "focal_point_key"),
                name="unique_rendition",
            )
        ]
