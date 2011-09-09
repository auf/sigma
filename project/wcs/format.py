# -*- encoding: utf-8 -*-

def str2civilite(self, s):
    output = s
    if s == 'M.':
        output = 'MR'
    elif s == 'Mme':
        output = 'MM'
    elif s == 'Mlle':
        output = 'ME'
    return output
    
def str2statutPersonne(self, s):
    """
    Exemple :
    pattern 1 (SIGMA) :
    1 Étudiant
    2 Chercheur
    3 Enseignant
    4 Enseignant-chercheur
    5 Post-Doc
    
    pattern 2:
    1 Chercheur
    2 Enseignant-chercheur
    3 Étudiant
    
    pattern 3:
    1 Étudiant
    2 Enseignant
    
    pattern 4:
    1 Étudiant
    2 Chercheur
    3 Enseignant-chercheur
    """
    output = 0  # équivalent du default dans sigma_v1.models.Dossier.statut
    if SIGMA_DOSSIER_STATUT_PERSONNE is not None :
        # si conf.py donne constante pour cet appel, pas de traitement
        output = SIGMA_DOSSIER_STATUT_PERSONNE
    else :
        try :
            # id du statut = permière lettre
            input = int(s[0])
            # WCS : valeurs différentes de SIGMA... :(
            if PATTERN_STATUT_PERSONNE is not None:
                if PATTERN_STATUT_PERSONNE == 1:
                    output = input
                elif PATTERN_STATUT_PERSONNE == 2:
                    if input == 1:
                        output = 2
                    elif input == 2:
                        output = 4
                    elif input == 3:
                        output = 1
                elif PATTERN_STATUT_PERSONNE == 3:
                    if input == 1:
                        output = 1
                    elif input == 2:
                        output = 3
                elif PATTERN_STATUT_PERSONNE == 4:
                    if input == 1:
                        output = 1
                    elif input == 2:
                        output = 2
                    elif input == 3:
                        output = 4
        except IndexError, ValueError :
            pass
    return output
    
def list2publicVise(self, l):
    """
    L'idée est de retrouver l'id SIGMA du public visé en fonction libellé
    passé.
     
    Valeurs SIGMA
    1 Etudiants
    2 Enseignant
    3 Chercheur
    4 Enseignant-Chercheur
    5 Post-Doc
    6 Professionnels non enseignants
    """
    # map entre values SIGMA et string reçus de WCS
    values = {
        'etudiants':1,
        'enseignant':2,
        'chercheur':3,
        'enseignant-chercheur':4,
        'post-doc':5,
        'professionnels non enseignants':6
    }
    output = 0  # équivalent du default dans sigma_v1.models.DossierMobilite.public_vise
    if l and type(l) == list:
        try:
            public = l[0]   # n'en prend qu'un car = FK dans modèle SIGMA... pas m2m
            key = public.lower()
            output = values[key]
        except KeyError:
            pass
    return output
       
def str2niveauEtude(self, s):
    """
    C_NIVEAU    L_INTITULE_NIVEAU   L_NIVEAU (annees)
    6               ...                 0
    1               Licence 2           2
    2               Licence 3           3
    3               Master 1            4
    4               Master 2            5
    7               Master 2 +          6
    5               Doctorat            8
    8               Bac + 7             7
    9               Doctorat            9
    """
    output = 0
    try :
        # années études = permière lettre
        annees = int(s[0])
        # sauf 10 ans = 2 premières lettres...
        if annees == 1:
            annees = 10
            
        if annees == 2 : output = 1
        elif annees == 3 : output = 2
        elif annees == 4 : output = 3
        elif annees == 5 : output = 4
        elif annees == 6 : output = 7
        elif annees == 7 : output = 8
        elif annees == 8 : output = 5
        elif annees == 9 : output = 9
        elif annees == 10 : output = 9
        
    except IndexError, ValueError :
        pass
    return output
    
def str2diplome(self, s):
    output = s
    if s.lower().startswith('autre'):
        output = '' # retourne vide car traitement teste si vide pour prendre valeur autre champ
    return output
    
def str2nbMois(self, s):
    output = 0
    try :
        # permière lettre = nb de mois
        output = int(s[0])
    except (ValueError, IndexError) :
        pass
    return output
    
def str2typeThese(self, s):
    output = s
    if s == 'Co-tutelle':
        output = 'CT'
    elif s == 'Co-direction':
        output = 'CD'
    elif s == 'Autre':
        output = 'AU'       
    return output
    
def str2bourse(self, s):
    """
    Exemple :
    input = Bourse de doctorat (Formation à la Recherche - FR)
    output = FR
    """
    pattern = r'.*(?P<code>\w{2})\)$'
    return self.code_from_pattern(pattern, s)

def str2pays(self, s):
    """
    Exemple :
    input = Arménie (AM - Europe centrale et orientale)
    output = AM
    """
    pattern = r'.*\((?P<code>\w{2}).*\)$'
    return self.code_from_pattern(pattern, s)

def str2etablissement(self, s):
    """
    Exemple :
    pattern 1 :
    input = Algérie - Centre universitaire d'El Oued (Sud/BEOM/1120)
    output = 1120
    
    pattern 2 :
    input = Cameroun - Université de Ngaoundéré (265 - Sud)
    output = 265
    """
    patterns = {
        1: r'.*\(.*/(?P<code>\d*)\)$',
        2: r'.*\((?P<code>\d*) .*\)$',
    }
    pattern = patterns[PATTERN_ETABL]
    return self.code_from_pattern(pattern, s)

def str2discipline(self, s):
    """
    Exemple :
    input = Anthropologie (D104)
    output = D104
    """
    pattern = r'.*\((?P<code>\w*)\)$'
    return self.code_from_pattern(pattern, s)

def str2date(self, s):
    date = None
    try:
        d = datetime.strptime(s, '%Y-%m-%d')
        date = datetime_date(d.year, d.month, d.day)
    except ValueError:
        pass
    return date
