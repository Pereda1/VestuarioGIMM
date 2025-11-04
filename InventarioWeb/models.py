from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class UsrsManager(BaseUserManager):
    def create_user(self, IdLogin, Secreto, **extra_fields):
        if not IdLogin:
            raise ValueError('El usuario debe tener un ID de login')
        
        user = self.model(
            IdLogin=IdLogin,
            **extra_fields
        )
        user.set_password(Secreto)
        user.save(using=self._db)
        return user

class Usrs(AbstractBaseUser):
    idUsrs = models.AutoField(primary_key=True)
    IdLogin = models.CharField(max_length=55, unique=True)
    Nombre = models.CharField(max_length=255, blank=True, null=True)
    Rol = models.IntegerField(blank=True, null=True)
    Secreto = models.CharField(max_length=200)
    Area = models.CharField(max_length=45, blank=True, null=True)
    Status = models.BooleanField(default=True)
    
    # Campos requeridos por AbstractBaseUser
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    objects = UsrsManager()
    
    USERNAME_FIELD = 'IdLogin'
    REQUIRED_FIELDS = ['Secreto']
    
    class Meta:
        db_table = 'Usrs'
    
    def __str__(self):
        return self.Nombre or self.IdLogin
    
    # Propiedad password para engañar a Django
    @property
    def password(self):
        return self.Secreto
    
    @password.setter
    def password(self, value):
        self.Secreto = make_password(value)
    
    # Métodos requeridos
    def set_password(self, raw_password):
        self.Secreto = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.Secreto)
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.Rol == 1
    
    # Para compatibilidad con el sistema de Django
    def get_username(self):
        return self.IdLogin

class Productos(models.Model):
    ID = models.AutoField(primary_key=True)
    CODIGO = models.CharField(max_length=50)
    ARTICULO = models.CharField(max_length=255)
    DISPVEST = models.IntegerField(null=True, blank=True)
    DISPMAQ = models.IntegerField(null=True, blank=True)
    DISPLAV = models.IntegerField(null=True, blank=True)
    DISPALM = models.IntegerField(null=True, blank=True)
    REQMUERTO = models.IntegerField(null=True, blank=True)
    CANT = models.IntegerField(null=True, blank=True)
    FECHAACT = models.DateTimeField(null=True, blank=True)
    DESCRIP = models.CharField(max_length=255, null=True, blank=True)
    MARCA = models.CharField(max_length=255, null=True, blank=True)
    IDFOTO = models.IntegerField(null=True, blank=True)
    Estatus = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'Productos'
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return f"{self.CODIGO} - {self.ARTICULO}"