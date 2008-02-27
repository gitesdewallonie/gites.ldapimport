# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from utils import normalizeString

class Proprietaire(object):
    """
    Un proprietaire
    """

    def getId(self):
        prenom = normalizeString(self.pro_prenom1[:3].lower())
        nom = normalizeString(self.pro_nom1[:3].lower())
        return "%s%s" % (prenom, nom)

    id = property(getId)

    def getEmail(self):
        mail = self.pro_email
        if not mail.strip():
            mail = 'michael.gdw@skynet.be'
        return mail

    email = property(getEmail)

    def getTitle(self):
        return "%s %s" % (self.pro_prenom1, self.pro_nom1)

    title = property(getTitle)
