# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from sqlalchemy import Table

from gites.ldapimport.importProprietaire import ImportProprietaire
from gites.ldapimport.proprietaire import Proprietaire
from gites.ldapimport.tests.base import LDAPImportTestCase

VERNIQ_LDIFF = """
dn: cn=verniq,ou=users,dc=gitesdewallonie,dc=net
cn: verniq
objectClass: person
objectClass: organizationalPerson
objectClass: gites-proprietaire
pk: 2
registeredAddress: vero@nique.be
sn: verniq
title: Vero Nique
"""

class ImportProprietaireTest(LDAPImportTestCase):
    def setUp(self):
        super(ImportProprietaireTest, self).setUp()
        self.importer = ImportProprietaire(self.pg, self.ldapConn)
        self.proprio = Table('proprio',
                             self.importer.pg.metadata)

    def tearDown(self):
        self.pg.truncate(self.proprio)
        super(ImportProprietaireTest, self).tearDown()

    def testUpdateLDAPWithoutExistingUsers(self):
        self._fillDB()
        result = self.importer.ldap.searchAll()
        self.assertEqual(result, [])
        self.assertRaises(AttributeError, self.importer.updateLDAP)

    def testUpdateLDAPWithExistingUsers(self):
        self._fillDB()
        self._fillLDAP(self.importer.ldap._connection)
        result = self.importer.ldap.searchAll()
        self.assertEqual(len(result), 1)
        self.importer.updateLDAP()
        result = self.importer.ldap.searchAll()
        self.assertEqual(len(result), 3)
        proprietaireGroup = self.importer.ldap.searchGroup('proprietaire')
        groupMembers = proprietaireGroup[0][1].get('uniqueMember')
        self.assertEqual(groupMembers, ['cn=jefroc,ou=users,dc=gitesdewallonie,dc=net',
                                        u'cn=jeabon,ou=users,dc=gitesdewallonie,dc=net',
                                        u'cn=verniq,ou=users,dc=gitesdewallonie,dc=net'])

    def testGetProprietaires(self):
        self._fillDB()
        session = self.importer.pg.getProprioSession()
        proprios = self.importer.getProprietaires(session)
        self.assertEqual(len(proprios), 3)

    def testCreateLdifWithoutPassword(self):
        self._fillDB()
        session = self.importer.pg.getProprioSession()
        proprio = session.query(Proprietaire).filter_by(pro_nom1 = u'Nique').one()
        self.assertEqual(proprio.pro_pass, u'')
        self.importer.createLdiff()
        session.refresh(proprio)
        self.assertNotEqual(proprio.pro_pass, u'')

    def testCreateLdiff(self):
        self._fillDB()
        self.failUnless(VERNIQ_LDIFF in self.importer.createLdiff())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ImportProprietaireTest))
    return suite
