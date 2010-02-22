# -=- encoding: utf-8 -=-
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend

from sigma.references.models import Bureau, Authentification
from sigma.www.models import RegionalGroup, Expert

from django.utils.translation import ugettext as _

import hashlib

class Permission:
    """Classe utilitaire permettant de gerer les droits et leurs descriptions"""
    tags = {'www.add_appel': _("Ajouter des appels d'offre"),
            'www.can_select_candidature': _("Selectionner des candidatures"),
            'www.can_classe_candidature': _("Classer des candidatures"),
            'www.add_candidature': _("Ajouter des candidatures"),
            'www.change_candidature' : _("Modifier des candidatures"),
            'www.change_appel' : _("Modifier des appels"),
            'www.admin': _("Administrer SIGMA")}
    
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        try:
            return Permission.tags[self.name]
        except:
            return self.name
        

class SettingsBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """
    def authenticate(self, username=None, password=None):
        #import pdb; pdb.set_trace()
        """Authentification de l'utilisateur

        @param username
        @param password
        """
        user = None
        try:
            user = self.as_expert(username, password)
        except Expert.DoesNotExist:
            user = None
        return user


    def as_user(self, username, password):
        """Authentification de l'utilisateur en tant qu'employe deja existant dans django

        @param auth
        """
        user = None
        user = User.objects.get(username=username)
        if settings.AUTH_PASSWORD_REQUIRED:
            if not user.check_password(password):
                raise User.DoesNotExist()
        if user.is_active:
            return user
        return None

    def as_employe(self, username, courriel, password):
        """Authentification de l'utilisateur en tant qu'employe et cree
        l'utilisateur django correspondant si c'est necessaire

        @param username
        @param password
        @param auth
        """
        password_md5 = hashlib.md5(password).hexdigest()
        user = None
        if not settings.AUTH_PASSWORD_REQUIRED:
            auth = Authentification.objects.get(courriel=courriel, actif=True)
        else:
            auth = Authentification.objects.get(courriel=courriel, motdepasse=password_md5, actif=True)
        try:
            # pas obligatoire que le id provenant de ref_authentification soit celui d'un Employe
            employe = auth.id
            first_name = employe.prenom
            last_name = employe.nom
        except Employe.DoesNotExist:
            employe = None
            first_name = ''
            last_name = ''
        try:
            user = self.as_user(courriel)
        except User.DoesNotExist:
            user = User(
                username=username, 
                email=auth.courriel,
                employe=employe,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,     # au sens django
                is_active=True,
                is_superuser = False    # au sens django
                )
            user.set_password(password)
            user.save()
        return user

    def as_expert(self, username, password):
        """Connexion en tant qu'expert au system

        @param username
        @param courriel
        @param password
        """
        user = None
        password_md5 = hashlib.md5(password).hexdigest()
        if not settings.AUTH_PASSWORD_REQUIRED:
            expert = Expert.objects.get(courriel=username, actif=True)
        else:
            expert = Expert.objects.get(courriel=username, motdepasse=password_md5, actif=True)
        try:
            user = self.as_user(username, password)
        except User.DoesNotExist:
            first_name=expert.prenom
            last_name=expert.nom
            user = User(
                username=username, 
                email=courriel,
                expert=expert,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,     # au sens django
                is_active=True,
                is_superuser = False    # au sens django
                )
            user.set_password(password)
            user.save()
        return user
            
    def as_admin(self, username, password):
        """Authentification de l'utilisateur en tant qu'administrateur

        @param username
        @param password
        """
        user = None

        if self.is_admin(username, password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                if settings.AUTOMATIC_ADMIN_CREATE:
                    # Create a new user. Note that we can set password
                    # to anything, because it won't be checked; the password
                    # from settings.py will.
                    user = User(username=username, password='get from settings.py')
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
        return user

    def is_admin(self, username, password):
        """Verifie que l'utilisateur, username, est l'administrateur et que
        son mot de passe correspond a notre configuration

        @param username Nom d'utilisateur
        @param password Mot de passe
        """
        return (settings.ADMIN_LOGIN == username) and \
            check_password(password, settings.ADMIN_PASSWORD)

    def get_rights(self, user):
        """Obtention des permissions accordees a un utilisateur

        @param user L'utilisateur a verifie
        @param (permissions, bureaux) Les permissions et les bureaux de 
               l'utilisateur
        """
        permissions = []
        bureaux = []

        if user.is_staff:
            permissions.append(Permission('www.add_appel'))
            permissions.append(Permission('www.can_select_candidature'))
            permissions.append(Permission('www.can_classe_candidature'))
            permissions.append(Permission('www.add_candidature'))
            permissions.append(Permission('www.admin'))
            bureaux = Bureau.objects.all()
        else:
            try:
                for permission in user.get_all_permissions():
                    permissions.append(Permission(permission))
                for group in user.groups.values_list():
                    (code, nom) = group
                    regional_group = RegionalGroup.objects.get(id=int(code))
                    bureaux.append(regional_group.bureau)
            except AttributeError:
                pass
        return (permissions, bureaux)
            
            
