# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.monomoy
