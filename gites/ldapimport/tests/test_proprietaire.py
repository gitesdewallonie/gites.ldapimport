# -*- coding: utf-8 -*-
"""
gites.ldapimport

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""
import unittest
from gites.ldapimport.proprietaire import Proprietaire
from gites.ldapimport.registry import PROPRIO_LOGIN_REGISTRY
class ProprietaireTest(unittest.TestCase):
    """
    Test the proprietaire behaviour
    """

    def testGetLogin(self):
        proprio1 = Proprietaire()
        proprio1.pro_prenom1 = 'Jean'
        proprio1.pro_nom1 = 'Bonn'
        proprio1.pro_log = ''
        proprio1.pro_etat = True
        self.assertEqual(proprio1.id, 'jeabon')
        self.assertEqual(proprio1.pro_log, 'jeabon')

    def testGetLoginWithoutNameSurname(self):
        proprio1 = Proprietaire()
        proprio1.pro_prenom1 = ''
        proprio1.pro_nom1 = ''
        proprio1.pro_log = ''
        proprio1.pro_etat = True
        self.assertNotEqual(proprio1.id, '')
        self.assertNotEqual(proprio1.pro_log, '')

    def testGetLoginWithExistingNameSurname(self):
        proprio1 = Proprietaire()
        proprio1.pro_prenom1 = 'Jean'
        proprio1.pro_nom1 = 'Bonne'
        proprio1.pro_log = ''
        proprio1.pro_etat = True
        PROPRIO_LOGIN_REGISTRY.append('jeabon')
        self.assertEqual(proprio1.id, 'jeabon-1')
        self.assertEqual(proprio1.pro_log, 'jeabon-1')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ProprietaireTest))
    return suite
