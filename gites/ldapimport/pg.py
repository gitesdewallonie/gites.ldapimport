# -*- coding: utf-8 -*-
"""
GitesLDAP

Licensed under the GPL license, see X for more details etc.
Copyright by Affinitic sprl

$Id$
"""
from sqlalchemy import create_engine, create_session
from sqlalchemy import BoundMetaData, mapper
from sqlalchemy.orm import clear_mappers
from gites.ldapimports.tables import getProprio

class Proprietaire(object):
    pass

class PGDB(object):
    def __init__(self, db_user, db_passwd, pg_host, pg_port, db_name,
                 table=None, table_columns=None):
        self.pg_string = 'postgres://%s:%s@%s:%s/%s' % (db_user, db_passwd,
                                                        pg_host, pg_port,
                                                        db_name)
        self.engine = create_engine(self.pg_string)
        self.table = table
        self.table_columns = table_columns

    def connect(self):
        self.db = self.engine.connect()
        self.metadata = BoundMetaData(self.engine)

    def setMappers(self):
        clear_mappers()
        self.proprio = getProprio(self.metadata)
        self.proprio.create(checkfirst=True)

        mapper(Proprietaire, self.proprio,
               primary_key=[self.proprio.c.pro_pk],)

    def getProprioSession(self):
        return create_session(bind_to=self.engine)

    def clearSession(self, session):
        session.flush()

    def disconnect(self):
        clear_mappers()
        self.db.close()
        del self.db
        del self.engine

