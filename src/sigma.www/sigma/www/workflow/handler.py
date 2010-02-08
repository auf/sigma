# -=- encoding: utf-8 -=-
from repoze.workflow import statemachine

from django.utils.translation import ugettext as _
from django.db import transaction

from sigma.www.workflow.logger import WorkflowLogger

def compose(*funcs):
    """Returns a function such that compose(a,b,c)(arg1, arg2, arg3)
    is equivalent to a(b(c(arg1, arg2, arg3))).
    
    @from http://bugs.python.org/file7762/functools.patch
    """
    def _composefunc(*args, **kw):
        l = reversed(funcs)
        rv = l.next()(*args, **kw)
        for f in l:
            rv = f(rv)
        return rv
    return _composefunc

class WorkflowError(statemachine.StateMachineError):
    """Définition d'une erreur standard du workflow"""
    pass

class Handler:
    """Représentation générique d'un gestionnaire de workflow pour les objets 
    du  modèle de données.

    Lorsqu'on veut définir un nouveau handler pour un des objets du modèle,
    il faut:

    # Se créer un nouveau module dans le dossier workflow
    # Créer une nouvelle classe héritant de Handler
    # Définir la variable de classe "classe" correspondant au type voulue
    # Définir chacune des transition à l'aide de la méthode "add" dans le init
    # Pour chaque transition, créer une méthode indépendante qui permet de 
      vérifier le bon passage à l'état
    # Définir les méthodes suivantes:
      - is_readable
      - can_add
    """
    
    # Classe associé au handler, c'est le type d'objet qui sera traité dans ce
    # workflow
    classe = object

    def __init__(self, user, name, init):
        """Défition des variables et des états de base nécessaire au bon 
        fonctionnement d'un workflow

        @param user Utilisateur courrant associé au workflow
        @param name Nom de l'attribut utilisé dans l'objet suivie
        @param init État initial des objets
        """
        self.user = user
        self.init = init
        self.logger = WorkflowLogger(user)
        self.sm = statemachine.StateMachine(name, initial_state=init)
        self.name = name
        self.final_states = []
        self.revert_actions = []
        self.post_functions = {}
        self.exporters = []
        self.errors = {}
        self.sm.after_transition = self.after_transition


    def add(self, from_state, action, to_state, transition):
        """Ajout d'une nouvelle étape de transition pour un type d'objets dans 
        le workflow qui est définie ici.

        @param from_state État initial
        @param action Nom de l'action de transition
        @param to_state État final
        @param transition méthode de vérification de la transition
        """
        self.sm.add(from_state, action, to_state, transition)
            

    def add_final(self, from_state, action, to_state, transition):
        """Ajout d'une nouvelle étape de transition final pour un type d'objets dans 
        le workflow qui est définie ici.

        @param from_state État initial
        @param action Nom de l'action de transition
        @param to_state État final
        @param transition méthode de vérification de la transition
        """
        self.add(from_state, action, to_state, transition)
        self.final_states.append(to_state)
        

    def add_revert(self, from_state, action, to_state, transition):
        """Ajout d'une nouvelle étape de transition pour en annuler une autre
        pour un type d'objets dans le workflow qui est définie ici.

        @param from_state État initial
        @param action Nom de l'action de transition
        @param to_state État final
        @param transition méthode de vérification de la transition
        """
        self.add(from_state, action, to_state, transition)
        self.revert_actions.append(action)


    def add_post(self, transition_id, function):
        """Ajout d'un post-traitement après le passage à un état quelquonque.

        @param transition_id Identificateur de la transition déclanchante
        @param function Fonction à exécuter
        """
        self.post_functions[transition_id] = function


    def add_exporter(self, exporter_class):
        """Ajout d'un nouvel exporter pour le type handler courant
        
        @param exporter_class
        """
        self.exporters.append(exporter_class)


    def _execute(self, context, transition_id, commentaires):
        """On reprend le code d'execution avec de le compose a notre code

        @param context Objet a execute
        @param transition_id Transition de l'objet
        """
        state = str(getattr(context, self.sm.state_attr, statemachine._marker))
        if state is statemachine._marker:
            state = str(self.sm.initial_state)
        si = (state, transition_id)
        sn = (state, None)
        newstate = None
        kw = {}
        # exact state match?
        if si in self.sm.states:
            if len(self.sm.states[si]) == 2:
                newstate, transition_fn = self.sm.states[si]
            else:
                newstate, transition_fn, kw = self.sm.states[si]
        # no exact match, how about a None (catch-all) match?
        elif sn in self.sm.states:
            newstate, transition_fn, kw = self.sm.states[sn]
        if newstate is None:
            raise statemachine.StateMachineError(
                'No transition from %r using transition %r'
                    % (state, transition_id))
        self.sm.before_transition(state, newstate, transition_id, context, **kw)

        a = compose(
            self.transition_before(state, newstate, transition_id, context, **kw),
            transition_fn(state, newstate, transition_id, context, **kw),
            self.transition_after(state, newstate, transition_id, context, commentaires, **kw))
        self.sm.after_transition(state, newstate, transition_id, context, **kw)

        setattr(context, self.sm.state_attr, newstate)


    def execute(self, ob, action, commentaires):
        """Méthode standard d'exécution d'une action
        
        @param ob Objet qui doit évoluer dans le workflow
        @param action Identificateur de la transition à exécuté
        """
        try:
            try:
                if action is None:
                    action = self.sm.transitions(ob).pop()
            except IndexError:
                raise WorkflowError("Aucune action executable")
            self._execute(ob, action, commentaires)
        except statemachine.StateMachineError, e:
            raise WorkflowError(e)
        return self.sm.state_of(ob)
        

    def undo(self, ob, commentaires):
        """Methode standard qui permet a un objet de revenir a un etat precedent

        @param ob
        """
        for log in self.logger.get(ob, WorkflowLogger.INFO, to_state=str(ob.statut)):
            for action in self.sm.transitions(ob, log.to_state):
                if self.sm.states[(ob.statut, action)][0] == log.from_state:
                    if action in self.revert_actions and self.is_reacheable(ob, action):
                        return self.execute(ob, action, commentaires)
        return self.sm.state_of(ob)


    def export(self, ob, export_type):
        """Exportation d'un objet vers un certains type de contenu en utilisant
        le gestionaire d'exportation générique. Notons que le type d'exportation
        doit être fournis au gestionaire afin de préciser ce qu'on veut.

        @param ob
        @param export_type
        """
        for exporter in self.exporters:
            if issubclass(exporter, export_type):
                return exporter(ob, self.user)()
        else:
            msg = _("Aucun exportateur %(export_type)s de ce type pour les %(experter)s")  % {'export_type': export_type, 'experter': self}
            raise AttributeError(msg)


    def transition_after(self, from_state, to_state, action, ob, commentaires):
        """Méthode appelé après la transition qui vérifie que tout s'est bien passée,
        soit qu'il n'y ait pas d'erreurs système et aucune erreur avec les critères
        qui ne puisse empêché le passage à un état suivant.

        Si c'est le cas, l'objet sera changé de statut et sauvegardé dans la base de données

        @param from_state État iniatial
        @param to_state État final
        @param action Id de transition
        @param ob Objet suivie dans le workflow
        """
        if len(self.logger.get(ob, WorkflowLogger.SYS, from_state, to_state)):
            raise WorkflowError("Impossible de passer %s à %s" % (from_state, to_state))
        elif len(self.logger.get(ob, WorkflowLogger.ERROR, from_state, to_state)):
            raise WorkflowError("Impossible de passer %s à %s" % (from_state, to_state))
        else:
            ob.statut = to_state
            ob.save()
            self.logger.info(ob, from_state, to_state, _("Passage reussi vers l'etat suivant"), commentaires)


    def transition_before(self, from_state, to_state, action, ob):
        """Méthode appelé avant la transition afin de s'assurer qu'aucune
        erreur de sera persisente.

        TODO: Est-ce vraiment pertinent et n'est-ce pas dommageable ?

        @param from_state État iniatial
        @param to_state État final
        @param action Id de transition
        @param ob Objet suivie dans le workflow
        """
        self.logger.clean(ob, WorkflowLogger.ERROR, from_state, to_state)


    def is_completed(self, ob):
        """Est-ce que le workflow est arrivé à un état final?

        @param ob Objet que l'on veut examiner
        """
        return str(ob.statut) in self.final_states


    def is_executable(self, ob):
        """Est-ce qu'il y a un état suivant executable pour l'objet,

        Ici on vérifie qu'il y a au moins une transition possible
        vers un autre état en vérifiant chacune des transitions
        disponible si elle est "reacheable".

        Notons que des transactions sont utilisées dans ces appels
        de fonctions afin de s'assurer que rien ne sera permanent.

        @param ob Objet que l'on veut examiner
        """
        action_list = self.sm.transitions(ob)
        if not action_list:
            return False
        for action in action_list:
            if self.is_reacheable(ob, action):
                if not action in self.revert_actions:
                    return True
        return False
        
    @transaction.commit_manually
    def is_reacheable(self, ob, action):
        """Est-ce que l'objet courant peut atteindre un état quelquonque, 

        Notons que tel que décrit dans la documentation du projet, des transactions
        sont utilisées ici afin de s'assurer qu'aucune erreur qui sera soulevé
        ici ne sera enregistré de façon permantente dans la base de données.

        On utilise donc les transactions manuelles pour cette raison

        @param ob Objet que l'on veut examiner
        @param action Identificateur de la transition que l'on veut executer
        """
        # afin de s'assurer que des transactions passées sont executées
        transaction.commit()

        from_state, transition, other = (0, 0, 0)
        reacheable = False

        try:
            try:
                (from_state, transition) = self.sm.states[(str(ob.statut), action)]
            except ValueError:
                (from_state, transition, other) = \
                    self.sm.states[(str(ob.statut),action)]
            kw = {}
            a = compose(
                self.transition_before(str(ob.statut), from_state, action, ob, **kw),
                transition(str(ob.statut), from_state, action, ob, **kw))

            sys = self.logger.get(ob, WorkflowLogger.SYS, str(ob.statut), from_state)
            errors = self.logger.get(ob, WorkflowLogger.ERROR, str(ob.statut), from_state)

            reacheable = len(sys) == 0 and len(errors) == 0
        except (KeyError, AttributeError):
            reacheable = False
        transaction.rollback()

        return reacheable


    @transaction.commit_manually
    def get_warnings(self, ob, action):
        """Est-ce que l'objet courant peut atteindre un état quelquonque, 

        Notons que tel que décrit dans la documentation du projet, des transactions
        sont utilisées ici afin de s'assurer qu'aucune erreur qui sera soulevé
        ici ne sera enregistré de façon permantente dans la base de données.

        On utilise donc les transactions manuelles pour cette raison

        @param ob Objet que l'on veut examiner
        @param action Identificateur de la transition que l'on veut executer
        """
        # afin de s'assurer que des transactions passées sont executées
        transaction.commit()

        from_state, transition, other = (0, 0, 0)
        warnings = []

        try:
            try:
                (from_state, transition) = self.sm.states[(str(ob.statut), action)]
            except ValueError:
                (from_state, transition, other) = \
                    self.sm.states[(str(ob.statut),action)]
            kw = {}
            a = compose(
                self.transition_before(str(ob.statut), from_state, action, ob, **kw),
                transition(str(ob.statut), from_state, action, ob, **kw))

            warnings = self.logger.get(ob, WorkflowLogger.WARNING, str(ob.statut), from_state)
            warnings = warnings.values('description', 'commentaires')

        except (KeyError, AttributeError):
            pass
        finally:
            transaction.rollback()

        return warnings

    @transaction.commit_manually
    def get_immediates(self, ob, action, level):
        """Est-ce que l'objet courant peut atteindre un état quelquonque, 

        Notons que tel que décrit dans la documentation du projet, des transactions
        sont utilisées ici afin de s'assurer qu'aucune erreur qui sera soulevé
        ici ne sera enregistré de façon permantente dans la base de données.

        On utilise donc les transactions manuelles pour cette raison

        @param ob Objet que l'on veut examiner
        @param action Identificateur de la transition que l'on veut executer
        """
        # afin de s'assurer que des transactions passées sont executées
        transaction.commit()

        from_state, transition, other = (0, 0, 0)
        logs = []

        try:
            try:
                (from_state, transition) = self.sm.states[(str(ob.statut), action)]
            except ValueError:
                (from_state, transition, other) = \
                    self.sm.states[(str(ob.statut),action)]
            kw = {}
            a = compose(
                self.transition_before(str(ob.statut), from_state, action, ob, **kw),
                transition(str(ob.statut), from_state, action, ob, **kw))

            logs = self.logger.get(ob, lebel, str(ob.statut), from_state)
            logs = logs.values('description', 'commentaires')

        except (KeyError, AttributeError):
            pass
        finally:
            transaction.rollback()

        return logs

    def is_valid(self, ob):
        """
        @param ob
        """
        return True

    def is_readable(self, ob):
        """Est-ce que l'objet ob est accessible à l'utilisateur courant
        
        Par défaut, aucun objet n'est accessible, il faut donc redéfinir cette
        fonction pour chaque handler

        @param ob Objet que l'on veut accéder
        """
        return False


    def is_undoable(self, ob):
        """Est-ce que l'objet ob peut etre revenir a un etat precedent
        
        @param ob
        """
        for log in self.logger.get(ob, WorkflowLogger.INFO, to_state=str(ob.statut)):
            for action in self.sm.transitions(ob, log.to_state):
                if self.sm.states[(ob.statut, action)][0] == log.from_state:
                    if action in self.revert_actions and self.is_reacheable(ob, action):
                        return True
        return False


    def get_logs(self, ob, level=WorkflowLogger.ERROR, from_state=None, to_state=None):
        """Obtention de ce qui empeche de passer d'un etat a un autre

        @param ob objet
        @param level
        @param from_state
        @param to_state
        """
        return self.logger.get(ob, level, from_state, to_state)


    def can_add(self, ob):
        """Est-ce que l'utilisateur courant peut ajouter des objets du type
        rechercher

        @param Classe ou instance du type d'objet que l'on veut créer
        """
        return False


    def can_edit(self, ob):
        """Est-ce que l'utilisateur courant peut edit des objets du type
        rechercher

        @param Classe ou instance du type d'objet que l'on veut créer
        """
        return False


    def after_transition(self, state, newstate, transition_id, context, **kw):
        """Méthode abstraite qui fait le filtrage des post_actions à exécuter
        selon le type de transition qui a été définit
 
        @param state État déclencheur
        @param newstate État de destination
        @param transition_id Idenficateur de la transition
        @param context Objet de workflow suivie
        @param **kw Autres paramètres
        """
        if transition_id in self.post_functions:
            self.post_functions[transition_id](context)


    def assert_sys(self, test, ob, from_state, to_state, error_message):
        """Verification qu'un objet repond a un critere systeme

        @param test
        @param ob
        @param from_state
        @param to_state
        @param error_message
        """
        if not test:
            self.logger.sys(ob, from_state, to_state, error_message)
        return test


    def assert_criteria(self, test, ob, from_state, to_state, error_message):
        """Verification qu'un objet repond a un critere du metier

        @param test
        @param ob
        @param from_state
        @param to_state
        @param error_message
        """
        if not test:
            self.logger.error(ob, from_state, to_state, error_message)
        return test    


    def assert_warn(self, test, ob, from_state, to_state, error_message, commentaire):
        """Verification qu'un objet repond a un critere leger du metier

        Ces erreurs ne seront pas preserver dans le cas d'une verifcation

        @param test
        @param ob
        @param from_state
        @param to_state
        @param error_message
        """
        if not test:
            self.logger.warning(ob, from_state, to_state, error_message, commentaire)
        return test
