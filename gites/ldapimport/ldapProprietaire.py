# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
import ldif
from StringIO import StringIO

from gites.ldapimport.interfaces import ILDAPProprietaire
from zope.interface import implements

BASE_DN = 'dc=gitesdewallonie,dc=net'

class LDAPProprietaire(object):
    """
    LDAP view on a proprietaire
    """
    implements(ILDAPProprietaire)

    def __init__(self, context):
        self.context = context

    def ldif(self):
        out = StringIO()
        ldifEntry = ldif.LDIFWriter(out)
        entry=dict(objectClass=['person', 'organizationalPerson',
                                'gites-proprietaire'],
                   cn=[self.context.id],
                   registeredAddress=[self.context.email],
                   pk=[str(self.context.pro_pk)],
                   title=[self.context.title],
                   userPassword=[self.context.password])
        dn = "cn=%s,%s" % (self.context.id, BASE_DN)
        ldifEntry.unparse(dn, entry)
        ldifContent = out.getvalue()
        out.close()
        return ldifContent

