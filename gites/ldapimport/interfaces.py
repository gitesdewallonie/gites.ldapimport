# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from zope.interface import Interface

class IProprietaire(Interface):
    """
    Proprietaire definition
    """

class ILDAPProprietaire(Interface):
    """
    LDAP view on a proprietaire
    """
