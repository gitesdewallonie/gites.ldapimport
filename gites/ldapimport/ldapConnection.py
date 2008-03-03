# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""

import ldap

class LDAP(object):
    """
    An ldap connection
    """
    def __init__(self, server, managerDn, managerPwd):
        """
        """
        self.server = server
        self.managerDn = managerDn
        self.managerPwd = managerPwd

    def connect(self):
        """
        """
        self._connection = ldap.initialize(self.server)
        self._connection.simple_bind(self.managerDn,
                                     self.managerPwd,
                                     ldap.AUTH_SIMPLE)

    def close(self):
        self._connection.unbind()

    def search(self, cn):
        base = "dc=net"
        scope = ldap.SCOPE_SUBTREE
        filterSearch = "(cn=jeff)"
        count = 0
        result_id = self._connection.search_s(base, scope, filterSearch)
        return
