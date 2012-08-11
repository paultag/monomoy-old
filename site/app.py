# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, render_template
from monomoy.db import db
import humanize

from bson.objectid import ObjectId

app = Flask(__name__)

@app.template_filter('humanize')
def _filter_humanize(date):
    return humanize.naturaltime(date)


@app.route("/")
def about():
    return render_template('about.html', **{})


@app.route("/jobs")
def index():
    jobs = db.jobs.find({})
    return render_template('jobs.html', **{
        "jobs": jobs
    })


@app.route("/builds")
def builds():
    changes = db.changes.find({})
    return render_template('builds.html', **{
        "changes": changes
    })


@app.route("/builders")
def builders():
    builders = db.builders.find({})
    return render_template('builders.html', **{
        "builders": builders
    })


@app.route("/build/<buildid>")
def build(buildid=None):
    builds = db.builds.find({"build": buildid})
    jobs = db.jobs.find({"build": buildid})

    return render_template('build.html', **{
        "builds": builds,
        "jobs": jobs
    })


if __name__ == "__main__":
    app.debug = True
    app.run()
