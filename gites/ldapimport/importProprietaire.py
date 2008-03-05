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
        ldifs = []
        for proprietaire in self.getProprietaires(session):
            ldapProprio = registry.queryAdapter(proprietaire,
                                                ILDAPProprietaire)
            ldifs.append(ldapProprio.ldif())
        session.flush()
        return "\n".join(ldifs)

    def updateLDAP(self):
        session = self.pg.getProprioSession()
        for proprietaire in self.getProprietaires(session):
            ldapProprio = registry.queryAdapter(proprietaire,
                                                ILDAPProprietaire)
            dn, entryAttributes = ldapProprio.extract()
            if self.ldap.searchUser(proprietaire.id):
                self.ldap.updateUser(dn, entryAttributes)
            else:
                self.ldap.addUser(dn, entryAttributes)
                self.ldap.addUserToGroup(dn, 'proprietaire')

def main():
    pg = PGDB('jfroche', 'xMLMY4', 'localhost', 5432, 'gites_wallons')
    ldap = LDAP('ldap://localhost', 'cn=admin,dc=gitesdewallonie,dc=net', 'phoneph0ne')
    proprioImport = ImportProprietaire(pg, ldap)
    proprioImport.connect()
    #proprioImport.createLdiff()
    proprioImport.updateLDAP()

if __name__ == "__main__":
    main()

