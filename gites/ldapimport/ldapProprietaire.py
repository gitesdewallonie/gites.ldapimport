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
from gites.ldapimport.ldapConnection import USER_BASE_DN

class LDAPProprietaire(object):
    """
    LDAP view on a proprietaire
    """
    implements(ILDAPProprietaire)

    def __init__(self, context):
        self.context = context

    def extract(self):
        """
        return dn and props
        """
        entryAttributes = dict(objectClass=['person', 'organizationalPerson',
                                            'gites-proprietaire'],
                   cn=[self.context.id],
                   registeredAddress=[self.context.email],
                   pk=[str(self.context.pro_pk)],
                   title=[self.context.title],
                   userPassword=[self.context.password])
        dn = "cn=%s,%s" % (self.context.id, USER_BASE_DN)
        return dn, entryAttributes

    def ldif(self):
        out = StringIO()
        ldifEntry = ldif.LDIFWriter(out)
        dn, entryAttributes = self.extract()
        ldifEntry.unparse(dn, entryAttributes)
        ldifContent = out.getvalue()
        out.close()
        return ldifContent

