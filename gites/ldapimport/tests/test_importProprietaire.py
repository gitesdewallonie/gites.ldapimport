# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from sqlalchemy import Table, create_engine
import unittest

from gites.ldapimport.importProprietaire import ImportProprietaire
from gites.ldapimport.pg import PGDB, Proprietaire
from gites.ldapimport.tables import getProprio

class ImportProprietaireTest(unittest.TestCase):
    def _createdb(self, pg):
        metadata = pg.metadata
        table = getProprio(metadata)
        table.create()

    def _fillDB(self):
        p1 = Proprietaire(1)
        p1.pro_prenom1 = u'Jean'
        p1.pro_nom1 = u'Bon'
        p1.pro_email = u'jean@bon.au'
        p2 = Proprietaire(2)
        p2.pro_prenom1 = u'Vero'
        p2.pro_nom1 = u'Nique'
        p2.pro_email = u'vero@nique.be'
        session = self.importer.pg.getProprioSession()
        session.save(p1)
        session.save(p2)
        session.flush()

    def setUp(self):
        pg = PGDB('user','pwd','host',0,'dbname', 'gites')
        pg.engine = create_engine('sqlite:///:memory:')
        pg.connect()
        pg.setMappers()
        self.importer = ImportProprietaire(pg)
        self.importer.pg = pg
        self.proprio = Table('proprio',
                             self.importer.pg.metadata)

    def testGetProprietaires(self):
        self._fillDB()
        proprios = self.importer.getProprietaires()
        self.assertEqual(len(proprios), 2)

    def testCreateLdiff(self):
        self._fillDB()
        self.importer.createLdiff()

    def tearDown(self):
        self.importer.pg.truncate(self.proprio)
        self.importer.pg.disconnect()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ImportProprietaireTest))
    return suite

if __name__ == '__main__':
    unittest.main()
