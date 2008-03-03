# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from gites.ldapimport.proprietaire import Proprietaire
from gites.ldapimport.pg import PGDB
from gites.ldapimport.ldapConnection import LDAP
from gites.ldapimport.interfaces import ILDAPProprietaire
from gites.ldapimport.registry import registry

class ImportProprietaire(object):
    """
    Import proprietaire to ldif format in ldap
    """

    def __init__(self, pg, ldap):
        self.pg = pg
        self.ldap = ldap

    def connect(self):
        self.pg.connect()
        self.pg.setMappers()
        self.ldap.connect()

    def getProprietaires(self, session):
        return session.query(Proprietaire).select()

    def createLdiff(self):
        session = self.pg.getProprioSession()
        for proprietaire in self.getProprietaires(session):
            ldapProprio = registry.queryAdapter(proprietaire,
                                                ILDAPProprietaire)
            ldapProprio.ldif()
        session.flush()

if __name__ == "__main__":
    pg = PGDB('jfroche', 'xMLMY4', 'localhost', 5432, 'gites_wallons')
    ldap = LDAP('ldap://localhost', 'dc=gitesdewallonie,dc=net', 'ph0neph0ne')
    prorioImport = ImportProprietaire(pg, ldap)
    prorioImport.connect()
    prorioImport.createLdiff()
