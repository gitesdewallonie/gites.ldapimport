# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from gites.ldapimport.proprietaire import Proprietaire
from gites.ldapimport.pg import PGDB

class ImportProprietaire(object):
    """
    Import proprietaire to ldif format in ldap
    """

    def __init__(self, pg):
        self.pg = pg

    def connect(self):
        self.pg.connect()
        self.pg.setMappers()

    def getProprietaires(self):
        session = self.pg.getProprioSession()
        return session.query(Proprietaire).select()

    def createLdiff(self):
        for proprietaire in self.getProprietaires():
            entry=dict(objectClass=['person', 'organizationalPerson',
                                    'gites-proprietaire'],
                       cn=[proprietaire.id],
                       registeredAddress=[proprietaire.email],
                       pk=[proprietaire.pro_pk],
                       title=[proprietaire.title])
            print entry


if __name__ == "__main__":
    pg = PGDB('jfroche', 'xMLMY4', 'localhost', 5432, 'gites_wallons')
    prorioImport = ImportProprietaire(pg)
    prorioImport.connect()
    prorioImport.createLdiff()
