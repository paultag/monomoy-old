# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from contextlib import contextmanager
from pbs import mailx, cat
import tempfile
import json
import os


settings = json.load(open("/etc/monomoy.mail", 'r'))
SERVER_ADMIN = settings['admin']


@contextmanager
def mail(subject, attachments):
    global SERVER_ADMIN
    subject = "[%s] %s" % (
        'monomoy',
        subject
    )

    fd, path = tempfile.mkstemp()
    yield path

    mailx(cat(path), "-s", str(subject), str(SERVER_ADMIN))
    os.remove(path)


def simple_mail(subject, body):
    global SERVER_ADMIN
    with mail(subject, []) as path:
        with open(path, 'w') as fd:
            fd.write(body)
