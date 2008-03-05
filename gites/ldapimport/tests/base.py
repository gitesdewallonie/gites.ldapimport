# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the <+ LICENSE +> license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""

from sqlalchemy import create_engine
from gites.ldapimport.tables import getProprio
from gites.ldapimport.proprietaire import Proprietaire
from gites.ldapimport.tests import fakeldap
from gites.ldapimport.ldapConnection import LDAP
from gites.ldapimport.pg import PGDB
from gites.ldapimport.registry import PROPRIO_LOGIN_REGISTRY
import unittest
import sys

# LDAP structure:
#
# gitesdewallonie.net
#    |
#    |-- groups
#    |   `-- Proprio
#    `-- users
#        `-- jeff

BASE ={'dc=net': [('cn', ['net'])],
       'dc=gitesdewallonie,dc=net': [('cn', ['gitesdewallonie'])],}

OU_BASE = {'ou=groups,dc=gitesdewallonie,dc=net':[('objectClass',
                                                   ['organizationalUnit']),
                                                     ('ou', ['groups']),],
           'ou=users,dc=gitesdewallonie,dc=net':[('objectClass',
                                                  ['organizationalUnit']),
                                                     ('ou', ['users']),]}

USERS = {'cn=jefroc,ou=users,dc=gitesdewallonie,dc=net':
         [('objectClass', ['person', 'organizationalPerson',
                           'gites-proprietaire']),
          ('cn', ['jefroc']),
          ('registeredAddress', ['jfroche@pyxel.be']),
          ('pk', ['444']),
          ('title', ['Jeff Roche']),
          ('userPassword', ['tototo'])]}

GROUPS = {'ou=proprietaire,ou=groups,dc=gitesdewallonie,dc=net':
         [('objectClass', ['groupOfUniqueNames',]),
          ('cn', ['Proprietaire']),
          ('ou', ['proprietaire']),
          ('uniqueMember', ['cn=jefroc,ou=users,dc=gitesdewallonie,dc=net'])]}

class LDAPImportTestCase(unittest.TestCase):
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
        self.pg = PGDB('user','pwd','host',0,'dbname', 'gites')
        self.pg.engine = create_engine('sqlite:///:memory:')
        self.pg.connect()
        self.pg.setMappers()
        self.ldapConn = LDAP('localhost','foo', 'bar')
        self.ldapConn._connection = fakeldap.FakeLDAPObject('dc=gitesdewallonie,dc=net')
        self._createLDAPStructure(self.ldapConn._connection)

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
        p3 = Proprietaire(3)
        p3.pro_prenom1 = u'Jeff'
        p3.pro_nom1 = u'Roche'
        p3.pro_email = u'jfroche@pyxel.be'
        p3.pro_pass = u'tototo'
        session = self.pg.getProprioSession()
        session.save(p1)
        session.save(p2)
        session.save(p3)
        session.flush()

    def _createLDAPStructure(self, ldapConnection):
        for dn, props in BASE.items():
            ldapConnection.add_s(dn, props)

        for dn, props in OU_BASE.items():
            ldapConnection.add_s(dn, props)

    def _fillLDAP(self, ldapConnection):
        for dn, props in USERS.items():
            ldapConnection.add_s(dn, props)

        for dn, props in GROUPS.items():
            ldapConnection.add_s(dn, props)

    def tearDown(self):
        fakeldap.clearLDAP()
        self.pg.disconnect()
        while PROPRIO_LOGIN_REGISTRY: PROPRIO_LOGIN_REGISTRY.pop()

