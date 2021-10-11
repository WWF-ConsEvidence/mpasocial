"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from api.urls import swagger_urls


API_TITLE = "MPA Social API"
API_DESCRIPTION = (
    "A Web API for accessing, creating and editing MPA social database records."
)
swagger_patterns = [path("api/", include(swagger_urls))]
schema_view = get_swagger_view(title=API_TITLE, patterns=swagger_patterns)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("docs/", include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path("swagger-docs/", schema_view),
    path("api-token-auth/", views.obtain_auth_token, name="api-token-auth"),
    path("rest-auth/", include("rest_auth.urls")),
]
