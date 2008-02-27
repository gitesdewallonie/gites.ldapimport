# -*- coding: utf-8 -*-
"""
GitesLDAP

Licensed under the GPL license, see X for more details etc.
Copyright by Affinitic sprl

$Id$
"""

from sqlalchemy import Table

def getProprio(metadata):
    return Table('proprio', metadata, autoload=True)

