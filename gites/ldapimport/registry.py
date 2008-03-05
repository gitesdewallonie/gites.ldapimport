# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from zope.interface.adapter import AdapterRegistry
from gites.ldapimport.interfaces import (IProprietaire,
                                         ILDAPProprietaire,
                                         INameChooser)
from gites.ldapimport.ldapProprietaire import LDAPProprietaire
PROPRIO_LOGIN_REGISTRY = []
from gites.ldapimport.namechooser import ProprietaireNameChooser


registry = AdapterRegistry()
registry.register([IProprietaire], ILDAPProprietaire, '', LDAPProprietaire)
registry.register([IProprietaire], INameChooser, '', ProprietaireNameChooser)
