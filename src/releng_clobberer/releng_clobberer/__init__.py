# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import click
import json
import os

import releng_clobberer.cli
import backend_common
import backend_common.db


DEBUG = bool(os.environ.get('DEBUG', __name__ == '__main__'))
HERE = os.path.dirname(os.path.abspath(__file__))
APP_SETTINGS = os.path.abspath(os.path.join(HERE, '..', 'settings.py'))


def init_app(app):
    return app.api.register(
        os.path.join(os.path.dirname(__file__), 'api.yml'))


if DEBUG and not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///%s' % (
        os.path.abspath(os.path.join(HERE, '..', 'app.db')))

if not os.environ.get('APP_SETTINGS') and \
       os.path.isfile(APP_SETTINGS):
    os.environ['APP_SETTINGS'] = APP_SETTINGS


app = backend_common.create_app(
    "releng_clobberer",
    extensions=[init_app, backend_common.db],
    debug=DEBUG,
    debug_src=HERE,
)


@app.cli.command()
def taskcluster_cache():
    workertypes = releng_clobberer.cli.taskcluster_cache()
    click.echo(json.dumps(workertypes, indent=2, sort_keys=True))


if __name__ == "__main__":
    app.run(**app.run_options())
