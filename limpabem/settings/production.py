import environ

from limpabem.settings.base import *
# Variaveis de ambiente
env = environ.Env()
environ.Env.read_env()

DEBUG = env.bool("DEBUG", False)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
DATABASES = {
    "default": env.db(),
}
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT")