# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""

import ldap
USER_BASE_DN = u"ou=users,dc=gitesdewallonie,dc=net"
GROUP_BASE_DN = u"ou=groups,dc=gitesdewallonie,dc=net"

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
        print self._connection.simple_bind(self.managerDn,
                                     self.managerPwd)

    def close(self):
        self._connection.unbind()

    def addUser(self, dn, userAttributes):
        attributes = [(key, item) for key, item in userAttributes.items()]
        return self._connection.add_s(dn, attributes)

    def addUserToGroup(self, dn, groupId):
        group = self.searchGroup(groupId)
        if not group:
            raise AttributeError, "Can't find group: %s" % groupId
        groupDn = group[0][0]
        uniqueMembers = group[0][1].get('uniqueMember', [])
        if dn not in uniqueMembers:
            uniqueMembers.append(str(dn))
        self._connection.modify_s(groupDn, [(ldap.MOD_REPLACE,
                                             'uniqueMember',
                                             uniqueMembers)])

    def updateUser(self, dn, userAttributes):
        attributes = [(ldap.MOD_REPLACE, key, item) for key, item in \
                      userAttributes.items()]
        return self._connection.modify_s(dn, attributes)

    def searchGroup(self, groupId):
        filterSearch = u"(ou=%s)" % groupId
        return self._connection.search_s(GROUP_BASE_DN, ldap.SCOPE_SUBTREE,
                                         filterSearch)

    def searchUser(self, userId):
        filterSearch = u"(cn=%s)" % userId
        return self._connection.search_s(USER_BASE_DN, ldap.SCOPE_SUBTREE,
                                         filterSearch)

    def searchAll(self):
        filterSearch = u"(objectClass=person)"
        return self._connection.search_s(USER_BASE_DN, ldap.SCOPE_SUBTREE,
                                         filterSearch)

