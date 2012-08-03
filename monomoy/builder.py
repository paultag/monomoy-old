# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from monomoy.db import db
import datetime as dt


def add_builder(**kwargs):
    ret = db.builders.insert(kwargs, safe=True)
    ping_from_builder(kwargs['_id'])
    return ret


def ping_from_builder(unique_id, **kwargs):
    payload = db.builders.find_one({"_id": unique_id}) or {}
    payload.update(kwargs)
    payload.update({
        "_id": unique_id,
        "lastping": dt.datetime.now()
    })
    return db.builders.update({"_id": unique_id},
                           payload,
                           False,  # Upsert
                           safe=True)


def get_builder(unique_id):
    return db.builders.find_one({"_id": unique_id}) or None


def delete_builder(unique_id):
    return db.builders.remove({"_id": unique_id}, safe=True)
