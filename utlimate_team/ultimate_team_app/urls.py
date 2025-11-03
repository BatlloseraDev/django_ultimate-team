from django.urls import path

from . import views



urlpatterns = [
    path('add_user', views.add_user),
    path('get_user/<int:id>', views.get_user),
    path('get_users', views.get_users),
    path('delete_user/<int:id>', views.delete_user),
    path('update_user/<int:id>', views.update_user),
]