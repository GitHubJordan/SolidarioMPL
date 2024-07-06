# solidario/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("admin/dashboard/", include('donations.urls_admin')),  # Inclui URLs do administrador
    path("", include("donations.urls")),  # Inclui URLs dos usuários
]
