import json
from application.model.render import Contents, Meta
from application import app


class Service(object):
    """
    Translates boto/S3 objects from 'storage' module
    into simple representations.
    """

    def __init__(self):
        if app.config['STORAGE'] == 's3':
            from storage.s3 import Storage
        elif app.config['STORAGE'] == 'db':
            from storage.db import Storage
        else:
            from storage.memory import Storage
        self.storage = Storage()
        app.logger.info("Storage is %s" % self.storage.__class__)

    def post(self, key, data):
        self.storage.post(key, data)

    def get(self, key, version=None):
        if version == 'list':
            lst = self.storage.list_versions(key)
            return json.dumps(
                {'versions': [Meta(ver).as_dict() for ver in lst]}
            )
        else:
            try:
                obj = self.storage.get(key, version)
                return Contents(obj).as_json()
            except Exception, e:
                print "Error", e
                return None

    def health(self):
        return self.storage.health()
