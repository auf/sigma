# -=- encoding: utf-8 -=-
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

pjc_base_path = 'candidatures'

def get_upload_path_pjc(instance, filename):
    """Stock les pieces jointes des candidatures dans un repertoire precis,
    dans media, tel que:

    pj_(id_PieceType)_(nom original avec des _).(extension)   
    """
    return os.path.join(pjc_base_path,
                        str(instance.candidature.id), 
                        'pj_%s_%s' % (instance.piecejointe.id , 
                                      filename.replace(' ', '_')))

        
