# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
from gites.ldapimport.tests.base import LDAPImportTestCase

class LDAPTest(LDAPImportTestCase):

    def testLDAPSearchAll(self):
        searchResult = self.ldapConn.searchAll()
        self.assertEqual(len(searchResult), 0)
        self._fillLDAP(self.ldapConn._connection)
        searchResult = self.ldapConn.searchAll()
        self.assertEqual(len(searchResult), 2)

    def testLDAPAddInUserOU(self):
        searchResult = self.ldapConn.searchAll()
        self.assertEqual(len(searchResult), 0)
        dn = 'cn=jeabon,ou=users,dc=gitesdewallonie,dc=net'
        userAttributes = {'registeredAddress': [u'jean@bon.au'],
                          'cn': [u'jeabon'],
                          'title': [u'Jean Bon'],
                          'objectClass': ['person', 'organizationalPerson',
                                          'gites-proprietaire'],
                          'pk': ['1'], 'userPassword': [u'x24eee']}
        self.ldapConn.addUser(dn, userAttributes)
        searchResult = self.ldapConn.searchAll()
        self.assertEqual(len(searchResult), 1)

    def testUpdateUser(self):
        self._fillLDAP(self.ldapConn._connection)
        result = self.ldapConn.searchUser('jefroc')
        self.assertEqual(result[0][1].get('registeredAddress'),
                         ['jfroche@pyxel.be'])
        userDn = result[0][0]
        userAttributes = dict(registeredAddress=['jfroche@affinitic.be'])
        self.ldapConn.updateUser(userDn, userAttributes)
        result = self.ldapConn.searchUser('jefroc')
        self.assertEqual(result[0][1].get('registeredAddress'),
                         ['jfroche@affinitic.be'])

    def testLDAPAddOutsideUserOU(self):
        dn = 'cn=verniq,dc=gitesdewallonie,dc=net'
        userAttributes = {'registeredAddress': [u'vero@nique.be'],
                          'cn': [u'verniq'], 'title': [u'Vero Nique'],
                          'objectClass': ['person', 'organizationalPerson',
                                          'gites-proprietaire'],
                          'pk': ['2'], 'userPassword': ['EtGiL6p']}
        self.ldapConn.addUser(dn, userAttributes)
        searchResult = self.ldapConn.searchAll()
        self.assertEqual(len(searchResult), 0)

    def testAddUserToUnexistingGroup(self):
        self._fillLDAP(self.ldapConn._connection)
        dn = 'cn=fakeuser,ou=users,dc=gitesdewallonie,dc=net'
        self.assertRaises(AttributeError, self.ldapConn.addUserToGroup ,
                          dn, 'unknownGroup')

    def testAddExistingUserToGroup(self):
        self._fillLDAP(self.ldapConn._connection)
        result = self.ldapConn.searchGroup('proprietaire')
        dn = 'cn=jefroc,ou=users,dc=gitesdewallonie,dc=net'
        self.assertEqual(result[0][1].get('uniqueMember'),
                         [dn])
        self.ldapConn.addUserToGroup(dn, 'proprietaire')
        result = self.ldapConn.searchGroup('proprietaire')
        self.assertEqual(result[0][1].get('uniqueMember'),
                         [dn])

    def testAddUserToGroup(self):
        self._fillLDAP(self.ldapConn._connection)
        dn = 'cn=fakeuser,ou=users,dc=gitesdewallonie,dc=net'
        result = self.ldapConn.searchGroup('proprietaire')
        self.assertEqual(result[0][1].get('uniqueMember'),
                         ['cn=jefroc,ou=users,dc=gitesdewallonie,dc=net'])
        self.ldapConn.addUserToGroup(dn, 'proprietaire')
        result = self.ldapConn.searchGroup('proprietaire')
        self.assertEqual(result[0][1].get('uniqueMember'),
                         ['cn=jefroc,ou=users,dc=gitesdewallonie,dc=net',
                          'cn=fakeuser,ou=users,dc=gitesdewallonie,dc=net'])

    def testLDAPSearch(self):
        self._fillLDAP(self.ldapConn._connection)
        searchResult = self.ldapConn.searchUser('jefroc')
        self.failUnless(searchResult)
        self.assertEqual(len(searchResult), 1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(LDAPTest))
    return suite
