# -=- encoding: utf-8 -=-
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms

from sigma.www import DEFAULT_SUBJECT

class SigmaModelForm(forms.ModelForm):
    """Nouveau type de formulaire pour les objets du modele qui permet de 
    mieux adapter ces types de formulaires a nos fonctionnalites tel que 
    le decoupage des champs par sujet
    """
    def __init__(self, *args, **kwargs):
        """Initialisation du formlulaire et des champs par sujet

        @param *args
        @param **kwargs
        """
        forms.ModelForm.__init__(self, *args, **kwargs)
        from sigma.www.utils import remove_accents

        self.subjects = []
        self.fields_by_subject = {}
        self.links = []

        for label, field in self.fields.items():
            if field.subject not in self.subjects:
                self.subjects.append(field.subject)
                
        for (tag, field) in self.fields.items():
            if field.subject not in self.fields_by_subject:
                self.fields_by_subject[field.subject] = SortedDict()
            self.fields_by_subject[field.subject][tag] = field

        for subject in self.subjects:
            label = remove_accents(mark_safe(subject.replace(" ", "_").replace("'", "_").replace(".","")))
            classes = ""
            for field in self.fields_by_subject[subject].keys():
                if field in self.errors.keys():
                    classes = "errortab"
                    break
            self.links.append((label, subject, classes))


    def as_p(self):
        """Nouvelle methode d'affichage des formulaires afin de regrouper 
        les champs en blocs de sujet
        """
        output = []
        fields_bk = self.fields
        from sigma.www.utils import remove_accents

        for subject, fields in self.fields_by_subject.items():
            self.fields = fields
        
            output.append("<div class='tab' id='tabs-%s'>" % remove_accents(mark_safe(subject.replace(' ', '_').replace("'", "_").replace(".",""))))
            output.append("<h2>%s</h2>" % subject)
            output.append("<table>")
            output.append(self._html_output(u"<tr><td valign='top'>%(label)s</td><td>%(field)s%(help_text)s</td></tr>", 
                                            u"<tr><td colspan='2'>%s</td></tr>", 
                                            u"</td></tr>", 
                                            u"<br />%s", True))
            output.append("<tr><td colspan='2'>")
            output.append("<label class='mandatory'>%s</label>" % _("* Les champs marqu&eacute; d'une asterisk sont obligatoires"))
            output.append("</td></tr>")
            output.append("</table>")
            output.append("</div>")

        self.fields = fields_bk
        return mark_safe(u'\n'.join(output))
