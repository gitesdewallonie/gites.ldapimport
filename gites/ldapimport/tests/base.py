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
       'dc=gitesdewallonie,dc=net': [('cn', ['gitesdewallonie'])], }

OU_BASE = {'ou=groups,dc=gitesdewallonie,dc=net': [('objectClass',
                                                   ['organizationalUnit']),
                                                     ('ou', ['groups']), ],
           'ou=users,dc=gitesdewallonie,dc=net': [('objectClass',
                                                  ['organizationalUnit']),
                                                     ('ou', ['users']), ]}

USERS = {'cn=jefroc,ou=users,dc=gitesdewallonie,dc=net':
         [('objectClass', ['person', 'organizationalPerson',
                           'gites-proprietaire']),
          ('cn', ['jefroc']),
          ('registeredAddress', ['jfroche@pyxel.be']),
          ('pk', ['444']),
          ('title', ['Jeff Roche']),
          ('userPassword', ['tototo'])],
         'cn=alameu,ou=users,dc=gitesdewallonie,dc=net':
         [('objectClass', ['person', 'organizationalPerson',
                           'gites-proprietaire']),
          ('cn', ['alameu']),
          ('registeredAddress', ['jfroche@pyxel.be']),
          ('pk', ['444']),
          ('title', ['Alain Meurant']),
          ('userPassword', ['tototo'])]}

GROUPS = {'ou=proprietaire,ou=groups,dc=gitesdewallonie,dc=net':
         [('objectClass', ['groupOfUniqueNames', ]),
          ('cn', ['Proprietaire']),
          ('ou', ['proprietaire']),
          ('uniqueMember', ['cn=jefroc,ou=users,dc=gitesdewallonie,dc=net'])]}


class LDAPImportTestCase(unittest.TestCase):

    def setUp(self):
        if '_ldap' in sys.modules:
            self.old_uldap = sys.modules['_ldap']
            del sys.modules['_ldap']
        else:
            self.old_uldap = None
        if 'ldap' in sys.modules:
            self.old_ldap = sys.modules['ldap']
            del sys.modules['ldap']
        else:
            self.old_ldap = None
        sys.modules['ldap'] = fakeldap
        self.pg = PGDB('user', 'pwd', 'host', 0, 'dbname', 'gites')
        self.pg.engine = create_engine('sqlite:///:memory:')
        self.pg.connect()
        self.pg.setMappers()
        self.ldapConn = LDAP('localhost', 'foo', 'bar')
        self.ldapConn._connection = fakeldap.FakeLDAPObject('dc=gitesdewallonie,dc=net')
        self._createLDAPStructure(self.ldapConn._connection)

    def _createdb(self, pg):
        metadata = pg.metadata
        table = getProprio(metadata)
        table.create()

    def _fillDB(self):
        p1 = Proprietaire()
        p1.pro_pk = 1
        p1.pro_etat = True
        p1.pro_prenom1 = u'Jean'
        p1.pro_nom1 = u'Bon'
        p1.pro_email = u'jean@bon.au'
        p1.pro_pass = u'x24eee'
        p1.pro_etat = True
        p2 = Proprietaire()
        p2.pro_pk = 2
        p2.pro_etat = True
        p2.pro_prenom1 = u'Vero'
        p2.pro_nom1 = u'Nique'
        p2.pro_email = u'vero@nique.be'
        p2.pro_pass = u''
        p2.pro_etat = True
        p3 = Proprietaire()
        p3.pro_pk = 3
        p3.pro_etat = True
        p3.pro_prenom1 = u'Jeff'
        p3.pro_nom1 = u'Roche'
        p3.pro_email = u'jfroche@pyxel.be'
        p3.pro_pass = u'tototo'
        p3.pro_etat = True
        p4 = Proprietaire()
        p4.pro_pk = 4
        p4.pro_prenom1 = u'Alain'
        p4.pro_nom1 = u'Meurant'
        p4.pro_email = u'alain@meurant.be'
        p4.pro_pass = u'tototo'
        p4.pro_etat = False
        session = self.pg.getProprioSession()
        session.add(p1)
        session.add(p2)
        session.add(p3)
        session.add(p4)
        session.flush()

    def _fillDuplicatesDB(self):
        p1 = Proprietaire()
        p1.pro_pk = 1
        p1.pro_etat = True
        p1.pro_prenom1 = u'Jeanne'
        p1.pro_nom1 = u'Bonne'
        p1.pro_email = u'jeanne@bonne.au'
        p1.pro_log = None
        p1.pro_pass = None
        p1.pro_etat = True
        p2 = Proprietaire()
        p2.pro_pk = 2
        p2.pro_etat = True
        p2.pro_prenom1 = u'Jean'
        p2.pro_nom1 = u'Bon'
        p2.pro_email = u'jean@bon.au'
        p1.pro_log = 'jeabon'
        p1.pro_pass = 'tototo'
        p2.pro_etat = True
        session = self.pg.getProprioSession()
        session.add(p1)
        session.add(p2)
        session.flush()

    def _createLDAPStructure(self, ldapConnection):
        for dn, props in BASE.items():
            ldapConnection.add_s(dn, props)

        for dn, props in OU_BASE.items():
            ldapConnection.add_s(dn, props)

    def _fillLDAP(self, ldapConnection, users=USERS):
        for dn, props in users.items():
            ldapConnection.add_s(dn, props)

        for dn, props in GROUPS.items():
            ldapConnection.add_s(dn, props)

    def tearDown(self):
        fakeldap.clearLDAP()
        self.pg.disconnect()
        while PROPRIO_LOGIN_REGISTRY:
            PROPRIO_LOGIN_REGISTRY.pop()
