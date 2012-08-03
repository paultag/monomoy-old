monomoy
=======

Monomoy is a dput'able package store (I use the phrase "package store" since
it's not compatable with apt, nor does it aim to be -- if you'd like something
that can host an apt repo, check out projects like dak, reprepro, or
mini-dinstall, depending on your needs.)

monomoy can hold processed package control files, has a lightweight queue
system, and aims to support remote builders accepting jobs based on their
registered abilities.

The idea here is to allow someone to dput a package into monomoy, and have
a crack-team of builders get to work verifying everything's OK on as much as
you can stand.

Monomy uses mongodb as the backend, for reasons I won't get into here.

license
-------

Monomoy is licensed under the widly used Expat license (which is one of the
many MIT family licenses)

I humbly request you be awesome and do awesome things.
