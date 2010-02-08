# -=- encoding: utf-8 -=-

from django.db import models

class Pays(models.Model):
    """Pays (donnée de référence, source: SQI).
    Liste AUF basée sur la liste ISO-3166-1.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=2, unique=True)
    code_iso3 = models.CharField(max_length=3, unique=True, blank=True)
    nom = models.CharField(max_length=255)
    region = models.ForeignKey(blank=True, null=True, to='Region', db_column='region')
    code_bureau = models.ForeignKey(blank=True, null=True, to='Bureau', to_field='code', db_column='code_bureau')
    nord_sud = models.CharField(max_length=255, blank=True)
    developpement = models.CharField(max_length=255, blank=True)
    monnaie = models.CharField(max_length=255, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_pays'

    def __unicode__(self):
        return u"%s (%s)" % (self.nom, self.code)

class Region(models.Model):
    """Région (donnée de référence, source: referentiels_spip).
    Une région est une subdivision géographique du monde pour la gestion de l'AUF.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    implantation_bureau = models.ForeignKey(blank=True, null=True, to='Implantation', db_column='implantation_bureau', related_name='gere_region')
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_region'

    def __unicode__(self):
        return u"%s (%s)" % (self.nom, self.code)

class Bureau(models.Model):
    """Bureau (donnée de référence, source: SQI).
    Référence legacy entre la notion de région et celle d'implantation responsable des régions et du central.
    Un bureau est :
    - soit le bureau régional d'une région (implantations de type 'Bureau')
    - soit la notion unique de Service central pour les 2 implantations centrales (implantations de type 'Service central' et 'Siege').
    Ne pas confondre avec les seuls 'bureaux régionaux'.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, blank=True)
    nom_long = models.CharField(max_length=255, blank=True)
    implantation = models.ForeignKey(blank=True, null=True, to='Implantation', db_column='implantation')
    region = models.ForeignKey(blank=True, null=True, to='Region', db_column='region')
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_bureau'

    def __unicode__(self):
        return u"%s (%s)" % (self.nom, self.code)

class Discipline(models.Model):
    """Discipline (donnée de référence, source: SQI).
    Une discipline est une catégorie de savoirs scientifiques.
    Le conseil scientifique fixe la liste des disciplines.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_long = models.CharField(max_length=255, blank=True)
    nom_court = models.CharField(max_length=255, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_discipline'

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.nom)

class Etablissement(models.Model):
    """Établissement (donnée de référence, source: GDE).
    Un établissement peut être une université, un centre de recherche, un réseau d'établissement...
    Un établissement peut être membre de l'AUF ou non.
    """

    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255)
    pays = models.ForeignKey(blank=True, null=True, to='Pays', to_field='code', db_column='pays')
    region = models.ForeignKey(blank=True, null=True, to='Region', db_column='region')
    implantation = models.ForeignKey(blank=True, null=True, to='Implantation', db_column='implantation', related_name='gere_etablissement')
    code_implantation = models.ForeignKey(blank=True, null=True, to='Implantation', to_field='code', db_column='code_implantation', related_name='code_gere_etablissement')
    # membership
    membre = models.BooleanField()
    membre_adhesion_date = models.DateField(null=True, blank=True)
    # responsable
    responsable_genre = models.CharField(max_length=1, blank=True)
    responsable_nom = models.CharField(max_length=255, blank=True)
    responsable_prenom = models.CharField(max_length=255, blank=True)
    # adresse
    adresse = models.CharField(max_length=255, blank=True)
    code_postal = models.CharField(max_length=20, blank=True)
    cedex = models.CharField(max_length=20, blank=True)
    ville = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    url = models.URLField(verify_exists=False, max_length=255, null=True, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_etablissement'

    def __unicode__(self):
        return u"%s - %s (%d)" % (self.pays.code, self.nom, self.id)

class Implantation(models.Model):
    """Implantation (donnée de référence, source: Implantus)
    Une implantation est un endroit où l'AUF est présente et offre des services spécifiques.
    Deux implantations peuvent être au même endroit physique.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    nom_court = models.CharField(max_length=255, blank=True)
    nom_long = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255)
    bureau_rattachement = models.ForeignKey(blank=True, null=True, to='Implantation', db_column='bureau_rattachement')
    region = models.ForeignKey(blank=True, null=True, to='Region', db_column='region')
    fuseau_horaire = models.CharField(max_length=255, blank=True)
    code_meteo = models.CharField(max_length=255, blank=True)
    # responsable
    responsable_implantation = models.IntegerField(null=True, blank=True)   # models.ForeignKey(blank=True, null=True, to='Employe')
    # adresse postale
    adresse_postale_precision_avant = models.CharField(max_length=255, blank=True)
    adresse_postale_no = models.CharField(max_length=30, blank=True)
    adresse_postale_rue = models.CharField(max_length=255, blank=True)
    adresse_postale_bureau = models.CharField(max_length=255, blank=True)
    adresse_postale_precision = models.CharField(max_length=255, blank=True)
    adresse_postale_boite_postale = models.CharField(max_length=255, blank=True)
    adresse_postale_ville = models.CharField(max_length=255)
    adresse_postale_code_postal = models.CharField(max_length=20, blank=True)
    adresse_postale_code_postal_avant_ville = models.NullBooleanField()
    adresse_postale_region = models.CharField(max_length=255, blank=True)
    adresse_postale_pays = models.ForeignKey('Pays', to_field='code', db_column='adresse_postale_pays', related_name='impl_adresse_postale')
    # adresse physique
    adresse_physique_precision_avant = models.CharField(max_length=255, blank=True)
    adresse_physique_no = models.CharField(max_length=30, blank=True)
    adresse_physique_rue = models.CharField(max_length=255, blank=True)
    adresse_physique_bureau = models.CharField(max_length=255, blank=True)
    adresse_physique_precision = models.CharField(max_length=255, blank=True)
    adresse_physique_ville = models.CharField(max_length=255)
    adresse_physique_code_postal = models.CharField(max_length=30, blank=True)
    adresse_physique_code_postal_avant_ville = models.NullBooleanField()
    adresse_physique_region = models.CharField(max_length=255, blank=True)
    adresse_physique_pays = models.ForeignKey('Pays', to_field='code', db_column='adresse_physique_pays', related_name='impl_adresse_physique')
    # autres coordonnées
    telephone = models.CharField(max_length=255, blank=True)
    telephone_interne = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    fax_interne = models.CharField(max_length=255, blank=True)
    courriel = models.EmailField(blank=True)
    courriel_interne = models.EmailField(blank=True)
    url = models.URLField(verify_exists=False, max_length=255, blank=True)
    # traitement
    statut = models.IntegerField()
    date_ouverture = models.DateField(null=True, blank=True)
    date_inauguration = models.DateField(null=True, blank=True)
    date_extension = models.DateField(null=True, blank=True, default='0000-00-00')
    date_fermeture = models.DateField(null=True, blank=True, default='0000-00-00')
    hebergement_etablissement = models.CharField(max_length=255, blank=True)    # models.ForeignKey(blank=True, null=True, to='Etablissement', db_column='hebergement_etablissement')
    hebergement_convention = models.NullBooleanField()
    hebergement_convention_date = models.DateField(null=True, blank=True)
    remarque = models.TextField()
    commentaire = models.CharField(max_length=255, blank=True)
    # meta
    actif = models.BooleanField()
    modif_date = models.DateField()

    class Meta:
        db_table = u'ref_implantation'

    def __unicode__(self):
        return u"%s (%d)" % (self.nom, self.id)

class Programme(models.Model):
    """Programme (donnée de référence, source: SQI).
    Structure interne par laquelle l'AUF exécute ses projets et activités, dispense ses produits et ses services.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    nom_long = models.CharField(max_length=255, blank=True)
    nom_court = models.CharField(max_length=255, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_programme'

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.nom)

class Projet(models.Model):
    """Projet (donnée de référence, source: CODA).
    C'est avec les projets que nous effectuons un suivi budgétaire, financier et qualitatif (indicateurs).
    Toute activité est rattachée à un projet (administrative ou de programme [produits/services]).
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    code_bureau = models.ForeignKey(blank=True, null=True, to='Bureau', to_field='code', db_column='code_bureau')
    code_programme = models.ForeignKey(blank=True, null=True, to='Programme', to_field='code', db_column='code_programme')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_projet'

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.nom)

class Poste(models.Model):
    """Poste (donnée de référence, source: CODA).
    Un poste est une catégorie destinée à venir raffiner un projet.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True)
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_poste'

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.code, self.nom, self.type)

class Authentification(models.Model):
    """Authentification"""
    id = models.ForeignKey('Employe', primary_key=True, db_column='id')
    courriel = models.CharField(max_length=255, unique=True)
    motdepasse = models.CharField(max_length=255)
    actif = models.BooleanField()
    
    class Meta:
        db_table = u'ref_authentification'
        ordering = ['id']
        
    def __unicode__(self):
        return u"%s [%d]" % (self.courriel, self.id.id)

class ProjetPoste(models.Model):
    """Projet-poste (donnée de référence, source: CODA).
    Un projet-poste consiste en une raffinement d'un projet par un poste (budgétaire).
    Subdivision utile pour le suivi budgétaire et comptable.
    """

    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    code_projet = models.ForeignKey(blank=True, null=True, to='Projet', to_field='code', db_column='code_projet')
    code_poste = models.ForeignKey(blank=True, null=True, to='Poste', to_field='code', db_column='code_poste')
    code_bureau = models.ForeignKey(blank=True, null=True, to='Bureau', to_field='code', db_column='code_bureau')
    code_programme = models.ForeignKey(blank=True, null=True, to='Programme', to_field='code', db_column='code_programme')
    # meta
    actif = models.BooleanField()

    class Meta:
        db_table = u'ref_projet_poste'

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.code_projet.nom)

class Service(models.Model):
    """Services (donnée de référence, source: SGRH).
    """
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255)
    actif = models.BooleanField()
    
    class Meta:
        db_table = u'ref_service'

    def __unicode__(self):
        return "%s" % (self.nom)

class PosteType(models.Model):
    """Postes types (donnée de référence, source: SGRH).
    """
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255)
    actif = models.BooleanField()
    
    class Meta:
        db_table = u'ref_poste_type'
        
    def __unicode__(self):
        return "%s (%s)" % (self.nom, self.id)


class Employe(models.Model):
    """Personne en contrat d'employé (CDD ou CDI) à l'AUF
    """
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    implantation = models.ForeignKey(to='Implantation', db_column='implantation', related_name='lieu_travail_theorique_de')    # SGRH
    implantation_physique = models.ForeignKey(to='Implantation', db_column='implantation_physique', related_name='lieu_travail_reel_de')
    courriel = models.CharField(max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=3)
    fonction = models.CharField(max_length=255, null=True, blank=True)
    telephone_poste = models.CharField(max_length=255, null=True, blank=True)
    telephone_ip = models.CharField(max_length=255, null=True, blank=True)
    responsable = models.ForeignKey(to='Employe', db_column='responsable', related_name='responsable_de', null=True, blank=True)
    mandat_debut = models.DateField(null=True, blank=True)
    mandat_fin = models.DateField(null=True, blank=True)
    date_entree = models.DateField(null=True, blank=True)
    service = models.ForeignKey('Service', db_column='service')
    poste_type_1 =  models.ForeignKey('PosteType', null=True, blank=True, db_column='poste_type_1', related_name='poste_type_1')
    poste_type_2 =  models.ForeignKey('PosteType', null=True, blank=True, db_column='poste_type_2', related_name='poste_type_2')
    # meta
    actif = models.BooleanField()
    
    class Meta:
        db_table = u'ref_employe'
        ordering = ['nom', 'prenom']
        
    def __unicode__(self):
        return u"%s, %s [%d]" % (self.nom.upper(), self.prenom, self.id)
        
    def getResponsable(self):
        """
        Retourne le responsable (objet employé) si il existe)
        Retourne None sinon
        """
        try :
            responsable = self.responsable
            if responsable:
                return responsable
        except Employe.DoesNotExist:
            return None        
        return None
        
    def isRecteur(self):
        """
        Teste si l'employé est le Recteur
        """
        poste = 6
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False

    def isDirecteurCabinet(self):
        """
        Teste si l'employé est le Directeur de Cabinet
        """
        poste = 1
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False
            
    def isSecretaireGeneral(self):
        """
        Teste si l'employé est le Secrétaire général
        """
        poste = 335
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False
        
    def isViceRecteurProgrammes(self):
        """
        Teste si l'employé est le Vice-Recteur au programme
        """
        poste = 8
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False
            
    def isAdmARI(self):
        """
        Teste si l'employé est l'Administrateur de l'ARI
        """
        poste = 339
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False
            
    def isAdmACCI(self):
        """
        Teste si l'employé est l'Administrateur de l'ACCI
        """
        poste = 203
        if self.poste_type_1_id==poste or self.poste_type_2_id==poste:
            return True
        return False

    # groupes
    @staticmethod
    def groupeTech():
        """
        Retourne le querySet de l'ensemble des employés techniques
        """
        listePosteTech = [21,22,46,48,56,276,301,308]
        return Employe.objects.filter(  \
                Q(poste_type_1__in=listePosteTech) | Q(poste_type_2__in=listePosteTech),  \
                Q(actif=True)   \
            )
        
    def isTech(self):
        """
        Teste si l'employé est un technicien de l'AUF
        """
        listePosteTech = [21,22,46,48,56,159,184,276,295,301,308,343]
#        21 Responsable technique local
#        22 Responsable technique régional
#        46 Responsable technique
#        48 Technicien bureautique
#        56 Technicien informatique
#       159 Technicien bureautique et chargé de la comptabilit...
#       184 Technicien de maintenance
#       276 Responsable des architectures techniques et du dép...
#       295 Gestionnaire comptable et technicien bureautique
#       301 Responsable technique régional et responsable tech...
#       308 Responsable et responsable technique local
#       343 Technicien supérieur en informatique
        if self.poste_type_1_id in listePosteTech or self.poste_type_2_id in listePosteTech:
            return True
        return False
        
    @staticmethod
    def groupeProgramme():
        """
        Retourne le querySet de l'ensemble des employés travaillant dans la ligne programme
        """
        listeServicesProgr = [12,13,16,20,21,22,23]
        return Employe.objects.filter(service__in=listeServicesProgr, actif=True)
    
    def isInGroupeProgrammes(self):
        """
        Le groupe programme est basé sur le service de l'employé :(
        """
        listeServicesProgr = [12,13,16,20,21,22,23]
    #    12  Programme « Langue française, diversité culturelle...
    #    13  Programme « Aspects de l'État de droit et démocrat...
    #    16  Programme « Environnement et développement durable...
    #    20  Programme « Renforcement de l'excellence universit...
    #    21  Programme « Innovations par les TIC pour l'éducati...
    #    22  Programme « Appropriation des outils technologique...
    #    23  Programmes
        if self.service.id in listeServicesProgr:
            return True
        return False
        
    def getAdmReg(self):
        """
        Retourne l'employé qui est l'Administrateur régional de la région de cet employé
        Retourne None si non applicable (Services centraux) ou inexistant
        """
        region = self.implantation.region
        try :
            implReg = [implantation.id for implantation in Implantation.objects.filter(region=region, actif=True)]
        except Implantation.DoesNotExist:
            implReg = []
            
        try :
            posteAdmReg = 285
            admReg = Employe.objects.filter(  \
                    Q(poste_type_1=posteAdmReg) | Q(poste_type_2=posteAdmReg),  \
                    Q(implantation__in=implReg),    \
                    Q(actif=True)   \
                )
            if admReg:
                return admReg[0]
        except Employe.DoesNotExist:
            return None        
        return None
        
    def getDdpReg(self):
        """
        Retourne l'employé qui est le Directeur délégué des programmes régional de la région de cet employé
        Retourne None si non applicable (Services centraux) ou inexistant
        """
        region = self.implantation.region
        try :
            implReg = [implantation.id for implantation in Implantation.objects.filter(region=region, actif=True)]
        except Implantation.DoesNotExist:
            implReg = []
            
        try :
            posteDdpReg = 334
            ddpReg = Employe.objects.filter(  \
                    Q(poste_type_1=posteDdpReg) | Q(poste_type_2=posteDdpReg),  \
                    Q(implantation__in=implReg),    \
                    Q(actif=True)   \
                )
            if ddpReg:
                return ddpReg[0]
        except Employe.DoesNotExist:
            return None        
        return None
