# -*- encoding: utf-8 -*-

from django.db import models

# Create your models here.
from sigma.models import Dossier

class BoursierCoda(models.Model):
    """
    Une personne attribue une note à un dossier de candidature.
    """
    boursier = models.ForeignKey(Dossier, verbose_name=u"Boursier", related_name="elements2")
    element2 = models.CharField(max_length=255,
                        verbose_name=u"Élément 2")
                        

class EcritureBoursier(models.Model):
    pcg = models.CharField(max_length=30)
    nom_pcg = models.CharField(max_length=150)
    code = models.CharField(max_length=30)
    elmlevel = models.IntegerField()
    name = models.CharField(max_length=300)
    sname = models.CharField(max_length=300)
    montanteur = models.DecimalField(max_digits=12, decimal_places=2)
    montantdoc = models.DecimalField(max_digits=12, decimal_places=2)
    devise = models.CharField(max_length=30)
    descr_ligne = models.CharField(max_length=300)
    doccode = models.CharField(max_length=60)
    descr_entete = models.CharField(max_length=300)
    date_doc = models.DateTimeField(null=True, blank=True)
    docnum = models.CharField(max_length=60)
    user = models.CharField(max_length=60)
    yr = models.IntegerField()
    period = models.IntegerField()
    paydate = models.DateTimeField()
    n_facture = models.CharField(max_length=60)
    n_avoir = models.CharField(max_length=60)
    imp_payeur = models.CharField(max_length=150)
    salarie = models.CharField(max_length=150)
    no_cheque = models.CharField(max_length=60)
    dc = models.CharField(max_length=60)
    statut_paiement = models.CharField(max_length=60)
    
    class Meta:
        db_table = u'ecriture_boursier'
        managed = False	 
