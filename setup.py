# -*- coding: utf-8 -*-
"""
<+ MODULE_NAME +>

Licensed under the <+ LICENSE +> license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id$
"""

from setuptools import setup, find_packages

setup(
    name = "gites.ldapimport",
    version = "0.2",
    author = "Jean Francois Roche",
    author_email = "jfroche@affinitic.be",
    description = "Import files from db",
    license = "GPL",
    keywords = "Affinitic libraries",
    url = 'http://svn.affinitic.be/python/gites.ldapimport',
    classifiers = [
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved"],
    packages = find_packages(),
    include_package_data = True,
    namespace_packages = ['gites'],
    zip_safe = False,
    install_requires = [
        'setuptools',
        'sqlalchemy',
        'psycopg2',
        'egenix-mx-base',
        'pysqlite',
        'python-ldap'
    ],
    )
