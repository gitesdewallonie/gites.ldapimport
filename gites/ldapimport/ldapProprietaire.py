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
from gites.ldapimport.utils import createLDAPPassword


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
        password = createLDAPPassword(str(self.context.password))
        entryAttributes = dict(objectClass=['person', 'organizationalPerson',
                                            'gites-proprietaire'],
                   cn=[self.context.id],
                   sn=[self.context.id],
                   registeredAddress=[str(self.context.email)],
                   pk=[str(self.context.pro_pk)],
                   title=[str(self.context.title)],
                   userPassword=[str(self.context.password)])
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
