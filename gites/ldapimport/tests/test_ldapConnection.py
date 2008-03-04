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
        self.assertEqual(len(searchResult), 1)

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
