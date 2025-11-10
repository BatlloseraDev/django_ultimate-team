from django.urls import path

from . import views



urlpatterns = [
    path('add_user', views.add_user, name='add_user'),
    path('get_user/<int:id>', views.get_user, name='get_user'),
    path('get_users', views.get_users, name='get_users'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('update_user/<int:id>', views.update_user, name='update_user'),
    path('asignar_equipo/<int:id>', views.asignar_equipo, name='asignar_equipo'),
    path('consultar_equipo/<int:id>', views.consultar_equipo, name='consultar_equipo'),
    path('asignar_rol/<int:id>', views.asignar_rol, name='asignar_rol'),
    path('eliminar_rol/<int:id>', views.eliminar_rol, name='eliminar_rol'),
    path('add_jugador', views.add_jugador,name='add_jugador'),
    path('get_jugador/<int:id>', views.get_jugador,name='get_jugador'),
    path('get_jugadores', views.get_jugadores,name='get_jugadores'),
    path('delete_jugador/<int:id>', views.delete_jugador,name='delete_jugador'),
    path('update_jugador/', views.update_jugador,name='update_jugador'),
    path('add_jugador_equipo/<int:id>', views.add_jugador_equipo,name='add_jugador_equipo'),
    path('delete_jugador_equipo/<int:id>', views.delete_jugador_equipo,name='delete_jugador_equipo'),
    path('media_total/<int:id_usuario>', views.media_total_equipo, name='media_total_equipo')

]