# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""

from affinitic.pwmanager.pwmanager import PasswordManager

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
        return session.query(Proprietaire).all()

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
                if proprietaire.pro_etat == False:
                    self.ldap.removeUser(dn)
                    continue
                else:
                    self.ldap.updateUser(dn, entryAttributes)
            else:
                if proprietaire.pro_etat == True:
                    self.ldap.addUser(dn, entryAttributes)
                    self.ldap.addUserToGroup(dn, 'proprietaire')
            session.add(proprietaire)
        session.flush()


def main():
    pg_pass = PasswordManager()
    pg_pass.registerFromFile('pgpass', 'pgpass', ':', None, True)
    pg_pass = pg_pass.getLoginPass()
    pg = PGDB(pg_pass[0], pg_pass[1], 'localhost', 5432, 'gites_wallons')

    ldap_pass = PasswordManager()
    ldap_pass.registerFromFile('ldappass', 'ldappass', ':', None, True)
    ldap_pass = ldap_pass.getLoginPass()
    ldap = LDAP('ldap://%s' % ldap_pass[0],
                'cn=admin,dc=gitesdewallonie,dc=net', ldap_pass[1])
    proprioImport = ImportProprietaire(pg, ldap)
    proprioImport.connect()
    #proprioImport.createLdiff()
    proprioImport.updateLDAP()

if __name__ == "__main__":
    main()
