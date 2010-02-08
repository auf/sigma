from django.db import models
from django.contrib.auth.models import User

from sigma.www.models import Region

class UserProfile(models.Model):
    """
    Profil d'un utilisation contenant des parametres supplementaires qui 
    permettent de stocker d'autres informations que les informations standard
    comme par exemple la region d'appartenance
    """
    user = models.ForeignKey(User, unique=True)
    region = models.ForeignKey(Region)
    
