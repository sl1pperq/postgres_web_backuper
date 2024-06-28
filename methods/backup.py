from models import Schema, File
from config import *
from tools import *


def make_db_backup(modes=['daily']):
    targets = Schema.query.all()

    objects = [(target.database, target.schema) for target in targets if target.freq in modes]
    tools = [Backuper(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT), Archiver(ZIP_PASSWORD)]  # ,
    # S3Uploader(S3_REGION, S3_access_key_id, S3_secret_access_key, S3_bucket, DEBUG)]

    for tool in tools:
        if DEBUG:
            print(objects, tool.__class__)
        objects = list(map(tool.db_apply, objects))


def make_file_backup(modes=['daily']):
    targets = File.query.all()

    objects = [(target.path) for target in targets if target.freq in modes]
    tools = [Archiver(ZIP_PASSWORD)]  # ,
    # S3Uploader(S3_REGION, S3_access_key_id, S3_secret_access_key, S3_bucket, DEBUG)]

    for tool in tools:
        if DEBUG:
            print(objects, tool.__class__)
        objects = list(map(tool.file_apply, objects))
