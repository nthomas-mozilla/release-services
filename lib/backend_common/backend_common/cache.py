# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from flask_cache import Cache


cache = Cache()


def init_app(app):
    cache_config = app.config.get('CACHE', {'CACHE_TYPE': 'simple'})
    cache.init_app(app, config=cache_config)
    return cache
