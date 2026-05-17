from django.urls import path
from . import views

urlpatterns = [

    # STUDENT
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login),
    path('exam/', views.view_exam),

    # ADMIN
    path('admin-login/', views.admin_login),
    path('dashboard/', views.dashboard),
    path('add-exam/', views.add_exam),
    path('admin-exam/', views.admin_view_exam),
    path('delete-exam/<int:id>/', views.delete_exam),

    # LOGOUT
    path('logout/', views.logout),
    path('admin-logout/', views.admin_logout),
]