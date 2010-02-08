# -=- encoding: utf-8 -=-
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from sigma.www.models import Expert
from sigma.www.forms import SigmaModelForm

class ExpertAjoutForm(SigmaModelForm):
      """Formulaire d'ajout d'un expert au systeme

      Notons que:
       * Pour chaque expert, plusieurs disciplines peuvent lui etre associees.
      """
      motdepasse = forms.CharField(widget=forms.PasswordInput)

      class Meta:
          model = Expert


class ExpertEditForm(SigmaModelForm):
      """Formulaire de modification d'un expert au systeme

      Notons que:
       * Pour chaque expert, plusieurs disciplines peuvent lui etre associees.
       * Nous maintenons plusieurs formulaire, 1 pour l'edition et l'autre pour 
         l'ajout afin de pouvoir limiter les parametres modifiable dans le futur.
      """
      class Meta:
          model = Expert

      def get_title(self):
          return "Modifier l'expert '%s %s' - %s" % (self.instance.prenom, 
                                                     self.instance.nom, 
                                                     self.instance.id)

      def get_action_url(self):
        return "/experts/edit/%s/" % self.instance.id
