# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import json
import sqlalchemy as sa

from backend_common.db import db

ALLOWED_REGIONS = ('us-east-1', 'us-west-1', 'us-west-2')


class File(db.Model):
    """An file, identified by size and digest.  The server may have zero
       or many copies of a file.
    """

    __tablename__ = 'releng_tooltool_files'

    id = sa.Column(sa.Integer, primary_key=True)
    size = sa.Column(sa.Integer, nullable=False)
    sha512 = sa.Column(sa.String(128), unique=True, nullable=False)
    visibility = sa.Column(sa.Enum('public', 'internal'), nullable=False)

    instances = sa.orm.relationship('FileInstance', backref='file')

    # note that changes to this dictionary will not be reflected to the DB;
    # add or delete BatchFile instances directly instead.
    @property
    def batches(self):
        return {bf.filename: bf.batch for bf in self._batches}

    def to_json(self, include_instances=False):
        file = dict(
            size=self.size,
            digest=self.sha512,
            algorithm='sha512',
            visibility=self.visibility,
            has_instances=any(self.instances)
        )
        if include_instances:
            file.instances = [i.region for i in self.instances]
        return json.dumps(file)


class FileInstance(db.Model):

    """A verified instance of a file in a single region."""

    __tablename__ = 'releng_tooltool_file_instances'

    file_id = sa.Column(sa.Integer, sa.ForeignKey('tooltool_files.id'), primary_key=True)  # noqa
    region = sa.Column(sa.Enum(*ALLOWED_REGIONS), primary_key=True)


class BatchFile(db.Model):

    """An association of upload batches to files, with filenames"""

    __tablename__ = 'releng_tooltool_batch_files'

    file_id = sa.Column(sa.Integer, sa.ForeignKey('tooltool_files.id'), primary_key=True)  # noqa
    file = sa.orm.relationship("File", backref="_batches")
    batch_id = sa.Column(sa.Integer, sa.ForeignKey('tooltool_batches.id'), primary_key=True)  # noqa
    batch = sa.orm.relationship("Batch", backref="_files")
    filename = sa.Column(sa.Text, nullable=False)


class Batch(db.Model):
    """Upload batches, with batch metadata, linked to the uploaded files.
    """

    __tablename__ = 'releng_tooltool_batches'

    id = sa.Column(sa.Integer, primary_key=True)
    uploaded = sa.Column(db.UTCDateTime, index=True, nullable=False)
    author = sa.Column(sa.Text, nullable=False)
    message = sa.Column(sa.Text, nullable=False)

    # note that changes to this dictionary will not be reflected to the DB;
    # add or delete BatchFile instances directly instead.
    @property
    def files(self):
        return {
            batch_file.filename: batch_file.file
            for batch_file in self._files
        }

    def to_json(self):
        return json.dumps(
            id=self.id,
            uploaded=self.uploaded,
            author=self.author,
            message=self.message,
            files={
                filename: file.to_json()
                for filename, file in self.files.iteritems()
            }
        )


class PendingUpload(db.Model):
    """Files for which upload URLs have been generated, but which haven't yet
       been uploaded.  This table is used to poll for completed uploads, and to
       prevent trusting files for which there is an outstanding signed upload
       URL.
    """

    __tablename__ = 'releng_tooltool_pending_upload'

    file_id = sa.Column(
        sa.Integer, sa.ForeignKey('tooltool_files.id'),
        nullable=False, primary_key=True)
    expires = sa.Column(db.UTCDateTime, index=True, nullable=False)
    region = sa.Column(
        sa.Enum(*ALLOWED_REGIONS), nullable=False)

    file = sa.orm.relationship('File', backref='pending_uploads')
