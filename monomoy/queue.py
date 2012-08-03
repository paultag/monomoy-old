# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from monomoy.builder import get_builder
from monomoy.db import db
import datetime as dt


def new_job(upload_id, requirements):
    return db.jobs.insert({
        "build": upload_id,
        "requirements": requirements,
        "entered": dt.datetime.now(),
        "builder": None
    },
    safe=True)


def next_job_by_req(requirements):
    if requirements == []:
        return None

    for job in db.jobs.find({"builder": None}).sort("entered", 1):
        valid = True
        for req in job['requirements']:
            if req not in requirements:
                valid = False
        if valid:
            return job


def next_job(unique_id):
    builder = get_builder(unique_id)
    if builder is None:
        return None

    return next_job_by_req(builder['capabilities'])


def take_job(unique_id):
    job = next_job(unique_id)
    if job is None:
        return { "err": "no new jobs" }

    job['builder'] = {
        "name": unique_id,
        "when": dt.datetime.now()
    }

    up = db.jobs.update({"_id": job['_id']},
                        job,
                        False,  #Upsert
                        safe=True)

    return job


def garbage_collect(how_old, builder_timeout):
    for job in db.jobs.find({"builder" : {"$ne" : None}}).sort("entered", 1):
        # Let's make sure the update is below the threshold
        if job['builder']['when'] < (
            dt.datetime.now() - dt.timedelta(seconds=how_old)
        ):
            print "Looking into %s" % (job['_id'])
            builder = get_builder(job['builder']['name'])
            if builder['lastping'] < (
                dt.datetime.now() - dt.timedelta(seconds=builder_timeout)
            ):
                print " -> builder timeout."
                db.jobs.update({"_id": job['_id']},
                               { "$unset" : {
                                   'builder' : 1
                               }},
                               False,  # upsert
                               False,  # multi
                               safe=True)
                print " -> removed builder lock."
            else:
                print " -> builder %s alive. Skipping." % (builder['_id'])
        else:
            print "Pending job: %s" % (job['_id'])
