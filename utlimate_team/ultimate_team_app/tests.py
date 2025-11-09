from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Rol


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
        url=reverse('update_user', args=[self.usuario.id])
        data = {
            "nombre":"Laura"
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombre, "Laura")
        self.assertEqual(response.status_code, 200)

    def test_actualizar_usuario_error(self):
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
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
            'rol':"usuario"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_asignar_rol_error(self):
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
                'rol':"gestor"
            }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)
