import boto3

from config import *
from datetime import datetime
from models import Backup
from backuper_server import db
from time import time

import os


class S3Uploader:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, bucket, debug=False):
        self.__session = boto3.session.Session()
        self.__bucket = bucket
        self.__aws_access_key = aws_access_key_id
        self.__debug = debug
        self.__s3 = self.__session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            region_name=str(region_name),
            aws_access_key_id=str(self.__aws_access_key),
            aws_secret_access_key=str(aws_secret_access_key),
        )

        self.__directory = datetime.now().strftime('%Y-%m-%d/%H_%M/')

    def apply(self, file_name):
        if not self.__debug:
            name = file_name.split('/')[-1]
            self.__s3.upload_file(file_name, self.__bucket, self.__directory + name)
            print(file_name, "uploaded")
        os.remove(file_name)
        print(file_name, "deleted!")
        return self.__directory + file_name.split('/')[-1]

    def remove(self, file_name):
        if not self.__debug:
            self.__s3.delete_object(file_name, self.__bucket, file_name)
            print(file_name, "deleted")


class S3Controler(S3Uploader):
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, bucket, pg_host: str, pg_port: int,
                 pg_user: str, pg_pass: str, debug=False):
        super().__init__(region_name, aws_access_key_id, aws_secret_access_key, bucket, debug)

    def db_apply(self, file_name):
        fname = self.apply(file_name)
        ct = time()
        db.session.add(Backup(path=fname, created=ct, lifetime=600))
        db.session.commit()

    def file_apply(self, file_name):
        fname = self.apply(file_name)
        db.session.commit()
