from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# UsuarioManager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener una dirección de correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('tipo_usuario', 'personal')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Modelo Usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('personal', 'Personal de Trabajo'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")  # Nuevo campo para nombre
    apellido = models.CharField(max_length=50, verbose_name="Apellido")  # Nuevo campo para apellido
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='cliente', verbose_name="Tipo de Usuario")
    
    # Campos adicionales requeridos para el sistema de autenticación
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()  # Aquí registramos el UsuarioManager

    USERNAME_FIELD = 'email'  # Establecemos el email como el campo de autenticación
    REQUIRED_FIELDS = ['nombre', 'apellido']  # Campos requeridos al crear un superusuario

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email} - {self.get_tipo_usuario_display()}"
