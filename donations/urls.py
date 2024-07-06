# donations/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from donations.views import custom_500_view, custom_404_view


urlpatterns = [
    path("register/", views.register, name="register"),
    path("register-donor", views.register_donor, name="register_donor"),
    path("login/", views.login, name="login"),
    path("accounts/login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("donate/", views.donate, name="donate"),
    path("items-for-sale/", views.items_for_sale, name='items_for_sale'),
    path("register-item/", views.item_donation_view, name="register_item"),
    path('validate-item/<int:item_id>/', views.validate_item, name='validate_item'),
    path('reject-item/<int:item_id>/', views.reject_item_view, name='reject_item_view'),
    path("thank-you/", views.thank_you, name='thank-you'),
    path("not-donor/", views.not_donor, name="not-donor"),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('news/', views.news_list, name='news_list'),
    path('activities/', views.activity_list, name='activity_list'),
    path("", views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = custom_500_view
handler404 = custom_404_view

