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
from gites.ldapimport.ldapConnection import LDAP
from gites.ldapimport.tables import getProprio

from gites.ldapimport.tests import fakeldap
import sys

GROUP_BASE = 'ou=groups,dc=gitesdewallonie,dc=net'
USERS = {'dc=net': [('cn', ['net'])],
         'dc=gitesdewallonie,dc=net': [('cn', ['gitesdewallonie'])],
         'cn=jeff,dc=gitesdewallonie,dc=net':
         [('objectClass', ['person', 'organizationalPerson',
                           'gites-proprietaire']),
          ('cn', ['jeff']),
          ('registeredAddress', ['jfroche@pyxel.be']),
          ('pk', ['444']),
          ('title', ['Jeff Roche']),
          ('userPassword', ['tototo'])]}


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
        p1.pro_pass = u'x24eee'
        p2 = Proprietaire(2)
        p2.pro_prenom1 = u'Vero'
        p2.pro_nom1 = u'Nique'
        p2.pro_email = u'vero@nique.be'
        p2.pro_pass = u''
        session = self.importer.pg.getProprioSession()
        session.save(p1)
        session.save(p2)
        session.flush()

    def setUp(self):
        if sys.modules.has_key('_ldap'):
            self.old_uldap = sys.modules['_ldap']
            del sys.modules['_ldap']
        else:
            self.old_uldap = None
        if sys.modules.has_key('ldap'):
            self.old_ldap = sys.modules['ldap']
            del sys.modules['ldap']
        else:
            self.old_ldap = None
        sys.modules['ldap'] = fakeldap
        pg = PGDB('user','pwd','host',0,'dbname', 'gites')
        pg.engine = create_engine('sqlite:///:memory:')
        pg.connect()
        pg.setMappers()
        ldapConn = LDAP('localhost','foo', 'bar')
        ldapConn._connection = fakeldap.FakeLDAPObject('dc=gitesdewallonie,dc=net')
        self.importer = ImportProprietaire(pg, ldapConn)
        self.proprio = Table('proprio',
                             self.importer.pg.metadata)
        #fakeldap.addTreeItems(GROUP_BASE)
        for dn, props in USERS.items():
            try:
                ldapConn._connection.add_s(dn, props)
            except:
                pass

    def testGetProprietaires(self):
        self._fillDB()
        session = self.importer.pg.getProprioSession()
        proprios = self.importer.getProprietaires(session)
        self.assertEqual(len(proprios), 2)

    def testCreateLdifWithoutPassword(self):
        self._fillDB()
        session = self.importer.pg.getProprioSession()
        proprio = session.query(Proprietaire).filter_by(pro_nom1 = u'Nique').one()
        self.assertEqual(proprio.pro_pass, u'')
        self.importer.createLdiff()
        session.refresh(proprio)
        self.assertNotEqual(proprio.pro_pass, u'')

    def testLDAPSearch(self):
        print self.importer.ldap.search('jeff')

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
