# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from utils import normalizeString, generatePassword
from zope.interface import implements
from gites.ldapimport.interfaces import IProprietaire

class Proprietaire(object):
    """
    Un proprietaire
    """
    implements(IProprietaire)

    def getId(self):
        if not bool(self.pro_log) or \
           self.pro_log == 'None' or self.pro_log == '0':

            prenom = normalizeString(self.pro_prenom1[:3].lower())
            nom = normalizeString(self.pro_nom1[:3].lower())
            self.pro_log = "%s%s" % (prenom, nom)
        return self.pro_log

    id = property(getId)

    def getEmail(self):
        mail = self.pro_email
        if not mail.strip():
            mail = u'michael.gdw@skynet.be'
        return mail

    email = property(getEmail)

    def getTitle(self):
        return "%s %s" % (self.pro_prenom1, self.pro_nom1)

    title = property(getTitle)

    def getPassword(self):
        if not bool(self.pro_pass) or \
           self.pro_pass == 'None' or self.pro_pass == '0':
            self.pro_pass = generatePassword(5)
        return self.pro_pass

    password = property(getPassword)


