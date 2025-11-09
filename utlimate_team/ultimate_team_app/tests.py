from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Rol, Posicion, Jugador, Nacionalidad, Equipo


# Create your tests here.
class AdminApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
            )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

    def test_crear_usuario_valido(self):
        """Comprobamos que se puede crear un usuario correctamente"""
        url = reverse('add_user')
        data = {
            "nombre": "Marta Frontón",
            "nick": "mfronton",
            "correo": "marta.fronton@example.com",
            "password": "12345",
            "rol": "administrador",
            "fecha_nacimiento": "2002-06-15",
            "fecha_registro": "2025-11-08",
            "equipo": 3
        }

        response = self.client.post(url, data=data, content_type="application/json")
        self.assertTrue(Usuario.objects.filter(nick='mfronton').exists())
        self.assertEqual(response.status_code, 201)

    def test_crear_usuario_error(self):
        """Al no dar un nombre no se permite crear la creación de un usuario"""
        url = reverse('add_user')
        data = {
            "nombre": "",  # nombre vacío
            "nick": "mfronton",
            "correo": "martafronton@example.com",
            "password": "12345",
            "rol": "administrador",
            "fecha_nacimiento": "2002-06-15"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_mostrar_usuarios_valido(self):
        """Comprobamos que se muestran todos los usuarios correctamente"""
        url=reverse('get_users')
        usuario=Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='martafronton@gmail.com',
            password="12345",
            fecha_nacimiento='2006-09-21'
        )
        usuario.rol.set([1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 2)

    def test_mostrar_usuarios_error(self):
        """Utilizar un método que no sea GET"""
        url = reverse('get_users')
        response = self.client.post(url)  # POST en vez de GET
        self.assertEqual(response.status_code, 405)

    def test_mostrar_usuario(self):
        """Comprobamos que podemos obtener un usuario por id"""
        url = reverse('get_user', args=[self.usuario.id])
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('marta', response.content.decode())

    def test_mostrar_usuario_invalido(self):
        """Intentamos obtener un usuario que no existe"""
        url = reverse('get_user', args=[999])  # ID que no existe
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_borrar_usuario(self):
        """Comprobamos que podemos borrar a un usuario correctamente"""
        url = reverse('delete_user', args=[self.usuario.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_borrar_usuario_invalido(self):
        """Intentamos borrar a un usuario que no existe"""
        url = reverse('delete_user', args=[999])  # ID que no existe
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_actualizar_usuario_valido(self):
        """Comprobamos que podemos actualizar el nombre de un usuario correctamente"""
        url=reverse('update_user', args=[self.usuario.id])
        data = {
            "nombre":"Laura"
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombre, "Laura")
        self.assertEqual(response.status_code, 200)

    def test_actualizar_usuario_error(self):
        """Intentamos actualizar un campo que no existe"""
        url=reverse('update_user', args=[self.usuario.id])
        data={
            "apellido":"Frontón"
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

class RolApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
        )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

    def test_asignar_rol_valido(self):
        """Comprobamos que podemos asignar roles a los usuarios correctamente"""
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
            'rol':"usuario"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_asignar_rol_error(self):
        """Intentamos asignar un rol que no existe a un usuario"""
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
                'rol':"gestor"
            }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

class UsuarioTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
        )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

        cls.pos_por, _ = Posicion.objects.get_or_create(tipo='POR', siglas='POR')
        cls.pos_def, _ = Posicion.objects.get_or_create(tipo='DEF', siglas='DEF')
        cls.pos_cen, _ = Posicion.objects.get_or_create(tipo='CEN', siglas='CEN')
        cls.pos_del, _ = Posicion.objects.get_or_create(tipo='DEL', siglas='DEL')


        cls.nacionalidad = Nacionalidad.objects.create(nombre='España')


        for i in range(3):
            Jugador.objects.create(nombre=f'Portero {i}', posicion_id=cls.pos_por, nacionalidad=cls.nacionalidad)
        for i in range(10):
            Jugador.objects.create(nombre=f'Defensa {i}', posicion_id=cls.pos_def, nacionalidad=cls.nacionalidad)
        for i in range(9):
            Jugador.objects.create(nombre=f'Centrocampista {i}', posicion_id=cls.pos_cen, nacionalidad=cls.nacionalidad)
        for i in range(6):
            Jugador.objects.create(nombre=f'Delantero {i}', posicion_id=cls.pos_del, nacionalidad=cls.nacionalidad)

    def test_asignar_equipo_valido(self):
        """Comprobamos que podemos asignar un equipo a un usuario correctamente"""
        url = reverse('asignar_equipo', args=[self.usuario.id])
        data={
          "nombre": "Argamasilla",
          "descripcion": "Equipo con espíritu competitivo"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_asignar_equipo_error(self):
        """Intentamos asignar un equipo a un usuario que ya tiene un equipo"""
        Equipo.objects.create(
            nombre="Equipo previo",
            id_usuario=self.usuario,
            descripcion="Equipo ya existente"
        )

        url = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_consultar_equipo_valido(self):
        """Comprobamos que podemos consultar el equipo de un usuario correctamente"""
        # Primero asignamos un equipo
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        url_consultar = reverse('consultar_equipo', args=[self.usuario.id])
        response = self.client.get(url_consultar, data={}, content_type="application/json")
        self.assertEqual(response.status_code, 200)



