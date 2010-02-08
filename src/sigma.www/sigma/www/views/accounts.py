from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import \
    login, \
    logout, \
    password_reset, \
    password_reset_done, \
    password_reset_confirm, \
    password_reset_complete, \
    password_change, \
    password_change_done
from django.contrib.auth.forms import PasswordResetForm 
from django.core.urlresolvers import reverse

from sigma.www.utils import render_to_response

"""
Vue de gestion de tout les aspects de la documentation
"""

def connexion(request, template_name='sigma.www/index.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """            
    return login(request, template_name, redirect_field_name)

def deconnexion(request, template_name='/', redirect_field_name=REDIRECT_FIELD_NAME):
    """ 
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Ou renvoyer ensuite
    @param redirect_field_name Ou renvoyer ensuite
    """
    return logout(request, template_name, redirect_field_name)


def pass_reset(request, template_name='sigma.www/password_reset_form.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_reset(request, is_admin_site=False, 
            template_name=template_name,
            email_template_name='sigma.www/password_reset_email.html',
            password_reset_form=PasswordResetForm, 
            post_reset_redirect=reverse('sigma.www.views.accounts.pass_reset_done'))


def pass_reset_done(request, template_name='sigma.www/password_reset_done.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_reset_done(request, template_name)


def pass_reset_confirm(request, uidb36=None, token=None, template_name='sigma.www/password_reset_confirm.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_reset_confirm(request,
            uidb36=uidb36,
            token=token, 
            template_name=template_name,
            post_reset_redirect=reverse('sigma.www.views.accounts.pass_reset_complete'),
            )


def pass_reset_complete(request, template_name='sigma.www/password_reset_complete.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_reset_complete(request,
            template_name=template_name,
            )


def pass_change(request, template_name='sigma.www/password_change_form.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_change(request,
            template_name=template_name,
            post_change_redirect=reverse('sigma.www.views.accounts.pass_change_done')
            )

def pass_change_done(request, template_name='sigma.www/password_change_done.html'):
    """
    Methode qui initie le processus d'affichage de la fenetre de connexion

    @param request La requete qui a ete recue
    @param template_name Le nom du template a utiliser
    @param redirect_field_name Ou renvoyer ensuite
    """
    return password_change_done(request,
            template_name=template_name,
            )
