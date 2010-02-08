# -=- encoding: utf-8 -=-
from StringIO import StringIO

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import models

import odf.text
import re
import os
import tempfile
import zipfile

from odf.element import Text
from odf import text
from odf.opendocument import load, OpenDocumentSpreadsheet
from odf import easyliststyle
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.table import Table, TableColumn, TableRow, TableCell, TableHeaderRows, TableHeaderColumns

from sigma.www import workflow

class GenericType(object):
    """Qu'est-ce qui definit ce qu'est un type d'exporteur"""

    def __unicode__(self):
        return export_type

    def __str__(self):
        return export_type

    def __cmp__(self,ob):
        return cmp(self.export_type, ob.export_type)


class ODFType(GenericType):
    """Exportion vers un fichier odf"""
    def __init__(self):
        self.export_type = "odf"


class MultiODFType(GenericType):
    """Exportion vers un fichier odf"""
    def __init__(self):
        self.export_type = "zip"

class MultiODSType(GenericType):
    """Exportion vers un fichier odf"""
    def __init__(self):
        self.export_type = "zip"

class ODSType(GenericType):
    """Exportation un fichier ods"""
    def __init__(self):
        self.export_type = 'ods'


class GenericExporter(object):
    """Generateur abstrait d'exportation d'exportations"""

    def __init__(self):
        raise NotImplementedError("This class is abstract")
    
        
    def __getattr__(self, attr):
        """On essaye de chercher la méthode dans la classe courante, 
        sinon dans la candidature

        @param attr L'attribut recherché
        """
        try:
            return self.__getattribute__(attr)
        except AttributeError :
            return lambda : getattr(self.obj, attr[1:])

    def __call__(self):
        """Racourci permettant de passer à travers toutes les étapes"""
        
        self.parse()

        return self.generate()

    def parse(self):
        """Methode de creation du contenu du document"""

        raise NotImplementedError("This class is abstract")

    def generate(self):
        """Methode de generation du document resultant de l'exportation"""

        raise NotImplementedError("This class is abstract")

    def getFilename(self):
        """Genere le nom du fichier"""
        raise NotImplementedError("This class is abstract")


class MultiCandidatureODFExporter(GenericExporter, MultiODFType):
    """Generateur d'un paquet de lettres type pour une liste de candidatures"""
    
    def __init__(self, candidature, user):
        self.obj = candidature
        self.user = user
        self.doc = StringIO()
        self.archive = zipfile.ZipFile(self.doc, 'w', zipfile.ZIP_DEFLATED)
    
    def parse(self):
        pass

    def generate(self):
        try:
            for candidature in self.obj:
                od = CandidatureODFExporter(candidature, self.user)
                od.parse()
                generated = od.generate()
                self.archive.writestr(od.getFilename(), generated)
        finally:
            self.archive.close()
        self.doc.seek(0)
        return self.doc.read()

    def getFilename(self):
        """Genere le nom du fichier"""
        return '%s-%s-lettre_type_candidatures-%s.zip' % (
            self.obj.appel.id, unicode(self.obj.appel).replace(" ","_"), self.obj.statut)
        

class CandidatureODFExporter(GenericExporter, ODFType):
    """Generateur de lettre type utilisant les placeholder au lieu d'un systeme 
    de tags personalise tel qu'utilise dans le passe"""

    DEFAULT_FILENAME = "_default.odt"

    def __init__(self, candidature, user):
        """
        @param candidature
        @param user
        """
        self.obj = candidature
        self.user = user
        self.filename = os.path.join(
            settings.DATA_DIRS[0], \
                "lettre_type", \
                self.getFilename())
        try:
            self.doc = load(self.filename)
        except IOError:
            self.filename = os.path.join(
                settings.DATA_DIRS[0],
                "lettre_type",
                CandidatureODFExporter.DEFAULT_FILENAME)
            self.doc = load(self.filename)
        self.regexp_text = re.compile(r'<([\S]*)>')


    def getFilename(self):
        """Genere le nom du fichier"""
        return '%s-candidatures-%s.odt' % (
            unicode(self.obj).replace(" ","_"), self.obj.statut)

    def parse(self):
        """Génération du document"""
        for holder in self.doc.getElementsByType(text.Placeholder):
            token = self.regexp_text.findall(holder.firstChild.data)
            if token:
                val = getattr(self, "_%s" % token[0])()
                older = holder.parentNode.parentNode
                parent = older.parentNode

                if parent.tagName == text.List().tagName:
                    parent.removeChild(older)

                    for li in val:
                        item = text.ListItem()
                        para = text.P(text=str(li))
                        item.appendChild(para)
                        parent.appendChild(item)
                else:
                    holder.parentNode.insertBefore(Text(val), holder)
                    holder.parentNode.removeChild(holder)

    def generate(self):
        """Génération du document odf"""
        h = StringIO()
        self.doc.write(h)
        h.seek(0)
        return h.read()

    def _raisons_preirrecevable(self):
        """Affichage des raisons du refus d'une candidature"""
        return workflow.Manager().get_logs(self.obj, self.user)


class GenericODSExporter(GenericExporter, ODSType):
    """Generateur generique de contenus ods pour les objets du modele"""

    def __init__(self, ob, user):
        """
        @param ob
        @param user
        """
        if isinstance(ob, models.Model):
            self.objs = [ob]
        else:
            self.objs = ob

        self.user = user
        self.doc = OpenDocumentSpreadsheet()

    def parse(self):
        """Generation du document"""
        tablecontents = Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
        self.doc.styles.addElement(tablecontents)

        widthshort = Style(name="Wshort", family="table-column")
        widthshort.addElement(TableColumnProperties(columnwidth="1.7cm"))
        self.doc.automaticstyles.addElement(widthshort)
        
        widthwide = Style(name="Wwide", family="table-column")
        widthwide.addElement(TableColumnProperties(columnwidth="1.5in"))
        self.doc.automaticstyles.addElement(widthwide)

        # extract the name of the class
        class_name = str(self.objs[0].__class__).split('.')[-1].strip("'>") 

        table = Table(name="%s(s)" % class_name)
        
        table.addElement(TableColumn(numbercolumnsrepeated=4,stylename=widthshort))
        table.addElement(TableColumn(numbercolumnsrepeated=3,stylename=widthwide))

        header = False

        for obj in self.objs:
            if not header:
                header = TableRow()
                table.addElement(header)
                for field in obj.serialisable_fields:
                    tc = TableCell()
                    header.addElement(tc)
                    p = text.P(stylename=tablecontents,text=field)
                    tc.addElement(p)

            tr = TableRow()
            table.addElement(tr)
            for field in obj.serialisable_fields:
                tc = TableCell()
                tr.addElement(tc)
                p = None
                try:
                    p = text.P(stylename=tablecontents,text=getattr(obj, field))
                except ObjectDoesNotExist:
                    try:
                        p = text.P(stylename=tablecontents,text=getattr(obj, '%s_id' % field))
                    except AttributeError:
                        p = text.P(stylename=tablecontents,text='')
                tc.addElement(p)                
            self.doc.spreadsheet.addElement(table)

    def generate(self):
        """Generation du fichier ods"""
        h = StringIO()
        self.doc.write(h)
        h.seek(0)
        return h.read()

    def getFilename(self):
        """Genere le nom du fichier"""
        if len(self.objs) == 1:
            return '%s-%s.ods' % (
                str(self.objs[0].__class__.__name__),
                str(self.objs[0]).replace(" ","_"))
        else:
            return '%s.ods' % (str(self.objs[0].__class__.__name__))

