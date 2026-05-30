from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from checker import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("profile/", views.profile, name="profile"),
    path("results/", views.results, name="results"),
    path("schemes/", views.scheme_list, name="scheme_list"),
    path("schemes/<slug:slug>/", views.scheme_detail, name="scheme_detail"),
]
