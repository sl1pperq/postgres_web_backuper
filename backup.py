# -*- coding: utf-8 -*-
from backuper_server import app
from methods import *

with app.app_context():
    make_db_backup(modes=['daily', 'weekly'])
