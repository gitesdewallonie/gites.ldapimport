# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from zope.interface.adapter import AdapterRegistry
from gites.ldapimport.interfaces import IProprietaire, ILDAPProprietaire
from gites.ldapimport.ldapProprietaire import LDAPProprietaire

registry = AdapterRegistry()
registry.register([IProprietaire], ILDAPProprietaire, '', LDAPProprietaire)

