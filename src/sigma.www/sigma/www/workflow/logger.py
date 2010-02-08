# -=- encoding: utf-8 -=-
from django.db import DatabaseError, IntegrityError
from django.contrib.auth.models import User, AnonymousUser

from sigma.www.models import WorkflowLog

class WorkflowLogger(object):
    """A logger which create logging information into the database"""

    ERROR = 1
    WARNING = 2
    INFO = 3
    SYS = 4

    def __init__(self, user):
        """ 
        @param user
        """
        self.user = user

    def error(self, ob, from_state, to_state, message, commentaires=None):
        """Log an error message to the logging process
        
        @param ob
        @param from_state
        @param to_state
        @param message
        """
        return self.log(ob, from_state, to_state, message, WorkflowLogger.ERROR, commentaires)


    def warning(self, ob, from_state, to_state, message, commentaires=None):
        """Log an error message to the logging process
        
        @param ob
        @param from_state
        @param to_state
        @param message
        """
        return self.log(ob, from_state, to_state, message, WorkflowLogger.WARNING, commentaires)


    def info(self, ob, from_state, to_state, message, commentaires=None):
        """Log an error message to the logging process
        
        @param ob
        @param from_state
        @param to_state
        @param message
        """
        return self.log(ob, from_state, to_state, message, WorkflowLogger.INFO, commentaires)


    def sys(self, ob, from_state, to_state, message, commentaires=None):
        """Log an error message to the logging process
        
        @param ob
        @param from_state
        @param to_state
        @param message
        """
        return self.log(ob, from_state, to_state, message, WorkflowLogger.SYS, commentaires)


    def log(self, ob, from_state, to_state, message, level, commentaires):
        """Ajout d'une erreur dans la structure des erreurs de transitions
        
        @param ob
        @param from_state
        @param to_state
        @param message
        @param level
        """
        try:
            log = WorkflowLog()

            log.objet = ob
            log.from_state=from_state
            log.to_state=to_state
            log.description=message

            if isinstance(self.user, AnonymousUser):
                log.user = None
            else:
                log.user = self.user

            log.level=level

            if commentaires is not None:
                log.commentaires = commentaires
            else:
                log.commentaires = ""

            log.save()

        except IntegrityError, e:
            # If there's already an error of this type
            # We don't need it another time
            return False
        else:
            return True

    def get(self, ob, level, from_state=None, to_state=None):
        """Obtention les logs d'un niveau d'un objet 

        @param ob
        @param from_state
        @param to_state
        @param level
        """
        if from_state is None and to_state is None:
            return WorkflowLog.objects.filter(objet=ob, level=level).order_by('timestamp')
        elif from_state is None:
            return WorkflowLog.objects.filter(objet=ob, to_state=to_state, level=level).order_by('timestamp')
        elif to_state is None:
            return WorkflowLog.objects.filter(objet=ob, from_state=from_state, level=level).order_by('timestamp')
        else:
            return WorkflowLog.objects.filter(objet=ob, from_state=from_state, to_state=to_state, level=level).order_by('timestamp')


    def clean(self, ob, level, from_state=None, to_state=None):
        """Suppression des logs d'un objet

        @param ob
        @param level
        @param from_state
        @param to_state
        """
        if from_state is None and to_state is None:
            WorkflowLog.objects.filter(objet=ob, level=level).delete()
        elif from_state is None:
            WorkflowLog.objects.filter(objet=ob, to_state=to_state, level=level).delete()
        elif to_state is None:
            WorkflowLog.objects.filter(objet=ob, from_state=from_state, level=level).delete()
        else:
            WorkflowLog.objects.filter(objet=ob, from_state=from_state, to_state=to_state).delete()
