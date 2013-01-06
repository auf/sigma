from haystack import indexes, site
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


class DossierIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    nom_complet = indexes.CharField(model_attr='candidat_nom_complet')

    def title(self):
        return 'asd'

    def summary(self):
        return 'asd asd asd dsa david'

    def index_queryset(self):
        return super(NoteIndex, self).index_queryset().filter(pub_date__lte=datetime.datetime.now())

# site.register(Allocataire, BaseModelSearchIndex)
# site.register(Allocation, BaseModelSearchIndex)
# site.register(FicheFinanciere, BaseModelSearchIndex)
# site.register(Expert, BaseModelSearchIndex)
# site.register(UserProfile, BaseModelSearchIndex)
# site.register(Appel, BaseModelSearchIndex)
# site.register(Candidat, BaseModelSearchIndex)
site.register(Dossier, indexes.ModelSearchIndex)
