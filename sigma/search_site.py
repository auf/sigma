from haystack import indexes, site
from django.contrib.auth.models import User
from sigma.boursiers.models import (
    Allocataire,
    Allocation,
    FicheFinanciere,
    )
from sigma.candidatures.models import (
    Expert,
    UserProfile,
    Appel,
    Candidat,
    Dossier,
    )


class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField()
    summary = indexes.CharField(use_template=True)

    def prepare_title(self, object):
        return repr(object)

    def index_queryset(self):
        return super(BaseIndex, self).index_queryset()
    

# site.register(Allocation, BaseModelSearchIndex)
# site.register(FicheFinanciere, BaseModelSearchIndex)
# site.register(Candidat, BaseIndex)
site.register(Allocataire, BaseIndex)
site.register(Appel, BaseIndex)
site.register(User, BaseIndex)
site.register(Expert, BaseIndex)
site.register(Dossier, BaseIndex)
