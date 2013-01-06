from haystack import indexes

# Utilise pour automatiquement creer le summary.
title_priority = [
    'titre',
    'prenom',
    'nom',
    'title',
    'name',
    '__repr__',
    ]

summary_priority = [
    'description',
    'nom_complet',
    ]

class Searcheable(object):
    def __get_attr_from_list(self, attr_list):
        found = None
        for attr in attr_list:
            if hasattr(self, attr):
                gotten = getattr(self, attr)
                if callable(gotten):
                    found = gotten()
                else:
                    found = gotten
            if found:
                break
        return found


    def title(self):
        return self.__get_attr_from_list(title_priority)
    
    def summary(self):
        return self.__get_attr_from_list(summary_priority)
