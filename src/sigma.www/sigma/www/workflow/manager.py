# -=- encoding: utf-8 -=-

from sigma.www.workflow.logger import WorkflowLogger

import django

class Manager(object):
      """Un gestionnaire de taches qui permet de stocker et de generer
      des workflows et leurs jobs associees."""


      class __impl(object):
            """Implantation du gestionnaire de de taches"""


            def __init__(self):
                self.handlers = {}


            def register(self, handler):
                  """Enregistrement d'un nouveau handler de workflow pour 
                  un objet du modele.
                  
                  @param handler Le nouvel handler à enregistrer
                  """
                  if handler.classe not in self.handlers:
                        self.handlers[handler.classe] = handler
                        return True
                  return False


            def get_handler(self, ob, user):
                  """Obtention du handler d'un objet ou d'une classe d'objets

                  @param ob Objet ou classe d'objets dont on veut le handler
                  @param user Utilisateur courant
                  """
                  try:
                        return self.handlers[ob.__class__](user)
                  except (AttributeError, KeyError):
                        return self.handlers[ob](user)
            

            def is_executable(self, ob, user):
                  """Verifie qu'on peut executer le workflow d'un objet en 
                  passant a l'etape suivante. Cela nous permet de nous assurer 
                  entre autre que:
                
                  * l'objet est suivi par un workflow
                  * le workflow de l'objet n'est pas termine
                  * les pre-requis de l'etape suivante sont remplis
                
                  @type   ob: django.models.* supporte par le taskmanager
                  @param  ob: Objet a executer
                  @rtype  Boolean
                  @return Est-ce qu'on peut passer a l'etape suivante du 
                          workflow d'un objet
                  """
                  return self.get_handler(ob, user).is_executable(ob)


            def execute(self, ob, user, action=None, commentaires=None):
                  """Complete la prochaine etape du workflow qui n'est pas 
                  deja execute.
                  
                  @type   ob: django.models.* supporte par le taskmanager
                  @param  ob: Objet a executer
                  @rtype  Boolean
                  @return Est-ce qu'on est passe a l'etape suivante
                  """
                  return self.get_handler(ob, user).execute(ob, action, commentaires)


            def undo(self, ob, user, commentaires=None):
                  """Fait revenir un objet a un etat precedent

                  @param ob
                  @param user
                  """
                  return self.get_handler(ob, user).undo(ob, commentaires)

            def export(self, ob, user, export_type):
                  """Exportation des donnes d'un objet du workflow
                  
                  @param ob
                  @param user
                  """
                  if isinstance(ob, django.db.models.Model):
                        return self.get_handler(ob, user).export(ob, export_type)
                  else:
                        return self.get_handler(ob[0], user).export(ob, export_type)


            def is_valid(self, ob, user):
                  """
                  @param ob
                  @param user
                  """
                  return self.get_handler(ob, user).is_valid(ob)


            def is_completed(self, ob, user):
                  """
                  Veirifie que pour un utilisateur, l'objet a termine son 
                  workflow.

                  @param ob Objet à inspecter
                  @param user utilisateur courant
                  @return Est-ce que l'objet est dans un statut complete
                  """
                  return self.get_handler(ob, user).is_completed(ob)


            def is_reacheable(self, ob, user, statut):
                  """Verifie que l'utilisateur courrant peut faire atteindre un 
                  statut à un objet.
                  
                  @param ob Objet que l'on veut inspecter
                  @param user Utilisateur courant
                  @param statut Statut à atteindre
                  """
                  return self.get_handler(ob, user).is_reacheable(ob, statut)


            def is_readable(self, ob, user):
                  """Verifie que l'objet peut etre acceder par l'utilisateur

                  @param ob Objet à inspecter
                  @param user Utilisateur courant
                  """
                  return self.get_handler(ob, user).is_readable(ob)


            def is_undoable(self, ob, user):
                  """Verifie que l'objet peut revenir a un etat precedent
                  
                  @param ob
                  @param user
                  """
                  return self.get_handler(ob, user).is_undoable(ob)


            def can_add(self, ob, user, *params):
                  """Verifie que l'utilisateur courant peut ajouter un 
                  nouvel objet.

                  @param ob Objet à inspecter ou classe
                  @param user Utilisateur courant
                  @param *params paramètres supplémentaires tel qu'un appel
                                 d'offres dans le cas de la classe Candidature
                  """
                  return self.get_handler(ob, user).can_add(*params)


            def can_edit(self, ob, user):
                  """Verifie que l'utilisateur courant peut editer objet

                  @param ob Objet à inspecter
                  @param user Utilisateur courant
                  @param *params paramètres supplémentaires tel qu'un appel
                                 d'offres dans le cas de la classe Candidature
                  """
                  return self.get_handler(ob, user).can_edit(ob) 


            def curr_statut(self, ob, user):
                  """Obtention du statut courant d'un objet

                  @param ob Objet à inspecter
                  @param user Utilisateur courant
                  """
                  return self.get_handler(ob, user).sm.state_of(ob)


            def prev_statut(self, ob, user):
                  """Obtention du statut precedent d'un objet

                  @param ob Objet à inspecter
                  @param user Utilisateur courant
                  """
                  p_states = []
                  handler = self.get_handler(ob, user)
                  for (p_state, p_transition) in handler.sm.states.keys():
                        (n_state, n_transition) = handler.sm.states[p_state, p_transition]
                        if n_state == ob.statut:
                              p_states.append(p_state)
                  return p_states


            def next_statut(self, ob, user):
                  """Obtention du ou des statuts suivant d'un objet

                  @param ob Objet à inspecter
                  @param user utilisateur courant
                  """
                  return self.get_handler(ob, user).sm.transitions(ob)


            def get_logs(self, ob, user, level=WorkflowLogger.ERROR, from_state=None, to_state=None):
                  """Obtention des erreurs qui se sont produites lors d'un
                  changement de statut d'un objet

                  @param ob
                  @param user
                  @param level
                  @param from_state
                  @param to_state
                  """
                  return self.get_handler(ob, user).get_logs(ob, level, from_state, to_state)


            def get_warnings(self, ob, user, action):
                  """
                  @param ob
                  @param user
                  @param action
                  """
                  return self.get_handler(ob, user).get_warnings(ob, action)
                  

            def get_immediates(self, ob, user, action, level=WorkflowLogger.ERROR):
                  """
                  @param ob
                  @param user
                  @param action
                  """
                  return self.get_handler(ob, user).get_immediates(ob, action, level)

      __instance = None

      def __init__(self):
            """Creation d'une instance du singleton"""
            # Verification si on a deja une instance de creee
            if Manager.__instance is None:
                  # Creation et sauvegarde d'une instance
                  Manager.__instance = Manager.__impl()
                  self.__dict__['_Manager__instance'] = Manager.__instance

      def __getattr__(self, attr):
            """ Delegation de l'acces aux attributs a l'implantation """
            return getattr(self.__instance, attr)
      
      def __setattr__(self, attr, value):
            """ Delegation de l'acces a l'implantation """
            return setattr(self.__instance, attr, value)

