# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from setuptools import find_packages, setup


with open('VERSION') as f:
    version = f.read().strip()


def read_requirements(file_):
    lines = []
    with open(file_) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('-e '):
                lines.append(line.split('#')[1].split('egg=')[1])
            elif line.startswith('#') or line.startswith('-'):
                pass
            else:
                lines.append(line)
    return lines


setup(
    name='mozilla-backend-common',
    version=version,
    description='Services behind https://mozilla-releng.net',
    author='Mozilla Release Engineering',
    author_email='release@mozilla.com',
    url='https://github.com/garbas/mozilla-releng',
    tests_require=read_requirements('requirements-dev.txt'),
    install_requires=read_requirements('requirements.txt'),
    extras_require=dict(
        api=['connexion'],
        auth=['Flask-Login', 'taskcluster'],
        cache=['Flask-Cache'],
        cors=['Flask-Cors'],
        db=['psycopg2', 'Flask-SQLAlchemy', 'Flask-Migrate'],
        log=['structlog', 'Logbook'],
        pulse=['kombu'],
        security=['flask-talisman'],
    ),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MPL2',
)
