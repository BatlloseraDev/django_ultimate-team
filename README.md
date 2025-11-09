# Django Ultimate Team
Proyecto grupal de Django realizado para el desafío de PAUF. Esta aplicación permite a los usuarios gestionar sus propios "Ultimate Teams" de fútbol.



# Instalación y Puesta en Marcha

1. **Clona el repositorio**
```bash
  git clone [https://github.com/BatlloseraDev/django_ultimate-team.git](https://github.com/BatlloseraDev/django_ultimate-team.git)
```
2. **Abrelo con el entorno virtual preferido**

    En este caso te recomiendo pycharm
3. **Dirigite a la direccion de la aplicación**
```bash
   cd .\utlimate_team\    
```    

4. **Aplica las migraciones**
```bash
   python manage.py migrate   
```  
5. **Inicia `load_init.py`**

    Para cargar los datos iniciales de la base de datos
```bash
   python manage.py load_ini 
```  
6. **Prueba distintos comandos**
```bash
  python manage.py carga_jugadores
  python manage.py carga_usuarios
```
7. **Inicia el servidor**
    En el arhivo `superusuario.txt` contiene un usuario de prueba para esta base de datos
```bash
   python manage.py runserver
```
---

# API de Usuarios y Equipos


## Tabla de endpoints

| Método | Ruta | Descripción | Body | Auth | Autor |
|--------|------|------------|------|------|-------|
| POST   | /add_user | Crea un nuevo usuario | JSON | — | Marta |
| GET    | /get_user/id_usuario/ | Devuelve un usuario por id | — | — | Marta |
| GET    | /get_users | Lista todos los usuarios | — | — | Marta |
| DELETE | /delete_user/id_usuario/ | Elimina un usuario por id | — | — | Marta |
| PUT    | /update_user/id_usuario/ | Actualiza los datos de un usuario | JSON | — | Marta |
| POST   | /asignar_equipo/id_usuario/ | Asigna un equipo a un usuario | JSON | — | Marta |
| GET    | /consultar_equipo/id_usuario/ | Consulta el equipo de un usuario | — | — | Marta |
| POST   | /asignar_rol/id_usuario/ | Asigna un rol a un usuario | JSON | — | Marta |
| DELETE | /eliminar_rol/id_usuario/ | Elimina un rol de un usuario | — | — | Marta |
| DELETE | /eliminar_rol_usuario | Elimina un rol de un usuario | JSON | — | Víctor |
| POST   | /crear_jugador | Crea un nuevo jugador | JSON | — | Víctor |
| PUT    | /modificar_jugador/id_jugador/ | Modifica los datos de un jugador | JSON | — | Víctor |
| DELETE | /eliminar_jugador | Elimina un jugador (soft delete)| — | — | Víctor |
| GET    | /mostrar_jugador/id_jugador/ | Muestra un jugador por id | — | — | Víctor |
| GET    | /mostrar_jugadores/ | Lista todos los jugadores | — | — | Víctor |
| POST   | /add_jugador/id_jugador | Asigna un jugador a un usuario | JSON | — | Víctor |

---

## Ejemplo de JSON para crear usuario
```json
{
  "nombre": "Luis González",
  "nick": "luiss",
  "correo": "luisgonzalez@gmail.com",
  "password": "12345",
  "rol": "usuario",
  "fecha_nacimiento": "2002-06-15",
  "fecha_registro": "2025-11-08"
}
```
---

## Ejemplo de JSON para actualizar usuario
```json
{
  "nombre": "Rocio",
  "nick": "ejemploNick"
}
```
---

## Ejemplo de JSON para asignar un equipo a un usuario

```json
{
  "nombre": "Argamasilla de Calatrava",
  "descripcion": "El mejor equipo"
}
```
---

## Ejemplo de JSON para asignar un rol a un usuario
```json
{
  "rol": "administrador"
}
```
## Ejemplo de JSON para eliminar un rol de un usuario
```json
{
  "rol": "administrador"
}
```
## Ejemplo de JSON para crear un jugador
```json
{
  "nombre": "Lionel Messi",
  "nacionalidad": "Argentina",
  "equipo": "Inter de Miami",
  "posicion_id": "Delantero",
  "pac": 90,
  "sho": 95,
  "pas": 88,
  "dri": 92,
  "defe": 30,
  "phy": 70
}
```
## Ejemplo de JSON para modificar datos de un jugador
```json
{
  "equipo": "Real Madrid",
  "posicion_id": "Delantero"
}
```
## Ejemplo de JSON para asignar un jugador a un usuario
```json
{
  "id_usuario": 2
}
```

## Creado por

Este proyecto fue desarrollado por:

* **Marta Frontón** - [@martafronton](https://github.com/martafronton)
* **Victor Albert Bat-Llosera** - [@BatlloseraDev](https://github.com/BatlloseraDev)

