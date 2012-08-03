# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

import os
import time
import json
import datetime
from bson.objectid import ObjectId


def parse_debcontrol(fil):
    payload = {}
    key = None

    for line in open(fil, 'r').readlines():
        if line[0] == " ":
            line = line.strip()
            if line == ".":
                payload[key] += "\n"
            else:
                payload[key] += line + "\n"
        else:
            line = line.strip()
            if line == "":
                continue

            key, value = line.split(":", 1)
            key = key.strip().lower()  # Treat all keys as lowercase.
            value = value.strip()
            payload[key] = value

    return payload


def parse_changes(fil):
    payload = parse_debcontrol(fil)

    newfiles = []
    for f in payload['files'].splitlines():
        hsh, size, section, prior, fd = f.split()
        newfiles.append({
            "hash": hsh,
            "size": size,
            "section": section,
            "priority": prior,
            "file": fd
        })
    payload['files'] = newfiles

    for sums in ["checksums-sha1", "checksums-sha256"]:
        newsums = []
        for line in payload[sums].splitlines():
            hsh, size, fd = line.split()
            newsums.append({
                "hash": hsh,
                "size": size,
                "file": fd
            })
        payload[sums] = newsums

    payload['architecture'] = payload['architecture'].split()

    return payload


def iter_dir(path):
    for f in os.listdir(path):
        yield "%s/%s" % (path, f)


def iter_dir_xtn(path, xtn):
    for f in iter_dir(path):
        if f[-len(xtn):] == xtn:
            yield f


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return time.mktime(obj.timetuple())
        return json.JSONEncoder.default(self, obj)
