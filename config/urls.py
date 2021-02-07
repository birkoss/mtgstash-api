from django.contrib import admin
from django.urls import path

from cards import views as cards_views


urlpatterns = [
    path('admin/', admin.site.urls),
]
