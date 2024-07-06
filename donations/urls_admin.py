# donations/ulrs_admin.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('donations/', views.admin_donation_list, name='admin_donation_list'),
    path('items/', views.admin_item_list, name='admin_item_list'),
    path('items-in-analysis/', views.admin_items_in_analysis, name='admin_items_in_analysis'),
    path('items-sold/', views.admin_items_sold, name='admin_items_sold'),
    path('funds/', views.admin_funds, name='admin_funds'),
    path('admin/register/', views.admin_register, name='admin_register'),

    # URLs de notícias
    path('admin/news/', views.admin_news_list, name='admin_news_list'),
    path('admin/news/create/', views.admin_news_create, name='admin_news_create'),
    path('admin/news/edit/<int:news_id>/', views.admin_news_edit, name='admin_news_edit'),
    path('admin/news/delete/<int:news_id>/', views.admin_news_delete, name='admin_news_delete'),

    # URLs de atividades
    path('admin/activities/', views.admin_activity_list, name='admin_activity_list'),
    path('admin/activities/create/', views.admin_activity_create, name='admin_activity_create'),
    path('admin/activities/edit/<int:activity_id>/', views.admin_activity_edit, name='admin_activity_edit'),
    path('admin/activities/delete/<int:activity_id>/', views.admin_activity_delete, name='admin_activity_delete'),
]