from xml.parsers.expat import model
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import PermissionDenied
from django.contrib import messages
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Usuário', max_length=30, unique=True)
    email = models.EmailField('E-mail', max_length=255)
    # type_user = models.BooleanField('Type of user', default=False)
    is_staff = models.BooleanField('Membro', default=False)
    is_superuser = models.BooleanField('Super user', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __exception_permission_denied(self, perm):
        if not perm in self.get_group_permissions():
            raise PermissionDenied()
        return True

    def check_permission(self, perm):
        try:
            if self.__exception_permission_denied(perm):    
                pass
        except PermissionDenied as e:
            return True

class Pessoa(Usuario):
    nome = models.CharField(max_length=255)
    logradouro = models.CharField(max_length=255)
    numero = models.IntegerField()
    cep = models.CharField(max_length=11)
    localidade = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField('CPF', max_length=15, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'pessoa'

class Gerente(Pessoa):
    class Meta:
        db_table = 'gerente'

class Atendente(Pessoa):
    class Meta:
        db_table = 'atendente'

