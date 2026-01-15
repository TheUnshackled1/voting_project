"""
URL configuration for voting_project project.
"""

from django.contrib import admin
from django.urls import path
from votes import views as votes_views


urlpatterns = [
    path("", votes_views.home, name="home"),
    path("login/", votes_views.login_view, name="login"),
    path("logout/", votes_views.logout_view, name="logout"),
    path("admin/", admin.site.urls),
]
