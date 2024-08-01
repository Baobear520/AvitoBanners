from django.db import models
from django.contrib.auth.models import AbstractUser


class AvitoUser(AbstractUser):
    """A base class for the whole Avito platform's user"""
    
    pass