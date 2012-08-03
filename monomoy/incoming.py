# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from monomoy.utils import (iter_dir_xtn, parse_changes,
                           parse_debcontrol, combine_array)

from monomoy.db import db
from monomoy.queue import new_job

import os


def get_path(pool, eyedee):
    return "%s/%s/%s/%s/%s" % (
        pool,
        eyedee[0],
        eyedee[1],
        eyedee[2],
        eyedee
    )


def reject(incoming_path, changes, fd):
    print "Rejecting %s" % (changes['source'])
    for fil in changes['files']:
        path = "%s/%s" % (incoming_path, fil['file'])
        os.unlink(path)
    os.unlink(fd)


def process_incoming(incoming_path, pool_path, settings):
    for fd in iter_dir_xtn(incoming_path, "changes"):
        changes = parse_changes(fd)

        if changes['architecture'] != ["source"]:
            # Reject.
            reject(incoming_path, changes, fd)
            continue

        key = db.changes.insert(changes, safe=True)

        print "Accepting %s as %s" % (
            changes['source'],
            str(key)
        )

        pool_folder = get_path(pool_path, str(key))
        os.makedirs(pool_folder)

        for fil in changes['files']:
            dsc = 'dsc'
            if fil['file'][-len(dsc):] == dsc:
                dscdata = parse_debcontrol("%s/%s" % (
                    incoming_path,
                    fil['file']
                ))

                db.controls.insert({
                    'changes': key,
                    'type': 'dsc',
                    'data': dscdata
                })

            path = "%s/%s" % (incoming_path, fil['file'])
            os.rename(path, "%s/%s" % (pool_folder, fil['file']))

        os.unlink(fd)

        for thing in combine_array(settings['build-for']):
            print new_job(str(key), thing)
