# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from utils import normalizeString, generateRandomLogin
from gites.ldapimport.registry import PROPRIO_LOGIN_REGISTRY

class ProprietaireNameChooser(object):
    """
    Name chooser: define the unique id of a proprietaire
    """

    def __init__(self, context):
        self.context = context
        self.count = 0

    def getPostLoginString(self):
        if self.count:
            return "-%s" % self.count
        else:
            return ''

    def getLogin(self):
        """
        return the unique login of the proprio
        """
        prenom = normalizeString(self.context.pro_prenom1[:3].lower())
        nom = normalizeString(self.context.pro_nom1[:3].lower())
        temp_pro_log = "%s%s%s" % (prenom, nom, self.getPostLoginString())
        if not temp_pro_log: # case where there is no prenom - nom
            temp_pro_log = generateRandomLogin()
        if temp_pro_log in PROPRIO_LOGIN_REGISTRY:
            self.count += 1
            temp_pro_log = self.getLogin()
        return temp_pro_log

