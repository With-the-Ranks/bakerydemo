import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from django.conf.urls.i18n import i18n_patterns
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView
from wagtail_ab_testing import urls as ab_testing_urls

from bakerydemo.search import views as search_views

from .api import api_router

urlpatterns = [
    path("django-admin/", admin.site.urls),
    # allauth endpoints
    path("accounts/", include("allauth.urls")),

    # force Wagtail admin login -> Google
    path("admin/login/", RedirectView.as_view(
        url="/accounts/google/login/?next=/admin/"
    )),

    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(),
        name="wagtailimages_serve",
    ),
    path("sitemap.xml", sitemap),
    path("api/v2/", api_router.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("abtesting/", include(ab_testing_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView
    from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(
            "favicon.ico",
            RedirectView.as_view(url=settings.STATIC_URL + "img/bread-favicon.ico"),
        )
    ]

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        path("test404/", TemplateView.as_view(template_name="404.html")),
        path("test500/", TemplateView.as_view(template_name="500.html")),
    ]

urlpatterns += i18n_patterns(
    path("search/", search_views.search, name="search"),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)
