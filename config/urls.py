from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

from blog.api import router as blog_router

# urls_namespace doc:
# https://django-ninja.rest-framework.com/guides/versioning/
api = NinjaAPI(urls_namespace='blog_api')
# Routers doc:
# https://django-ninja.rest-framework.com/guides/routers/
api.add_router("/blog/", blog_router)

urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),
    # API urls
    path("api/v1/", api.urls),
]
