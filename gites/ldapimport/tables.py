# -*- coding: utf-8 -*-
"""
GitesLDAP

Licensed under the GPL license, see X for more details etc.
Copyright by Affinitic sprl

$Id$
"""

from sqlalchemy import Table, Column, String, Integer, Index

def getProprio(metadata):
    autoload = False
    if metadata.engine.has_table('proprio'):
        autoload = True
    proprio = Table('proprio', metadata,
                 Column(u'pro_pk', Integer(), primary_key=True),
                 Column(u'pro_nom1', String()),
                 Column(u'pro_nom2', String()),
                 Column(u'pro_prenom1', String()),
                 Column(u'pro_prenom2', String()),
                 Column(u'pro_societe', String()),
                 Column(u'pro_adresse', String()),
                 Column(u'pro_email', String()),
                 Column(u'pro_tel_priv', String()),
                 Column(u'pro_tel_bur', String()),
                 Column(u'pro_fax_priv', String()),
                 Column(u'pro_fax_bur', String()),
                 Column(u'pro_gsm1', String()),
                 Column(u'pro_gsm2', String()),
                 Column(u'pro_url', String()),
                 Column(u'pro_tva', String()),
                 Column(u'pro_comment', String()),
                 Column(u'pro_etat', String()),
                 Column(u'pro_desact_comment', String()),
                 Column(u'pro_desact_justif', String()),
                 Column(u'pro_date_in', String()),
                 Column(u'pro_date_out', String()),
                 Column(u'pro_motif_out', String()),
                 Column(u'pro_justif_out', String()),
                 Column(u'pro_langue', String()),
                 Column(u'pro_log', String()),
                 Column(u'pro_pass', String()),
                 Column(u'pro_com_fk', Integer()),
                 Column(u'pro_civ_fk', Integer()), autoload=autoload)
    Index('proprio_pkey', proprio.c.pro_pk, unique=True)
    return proprio

