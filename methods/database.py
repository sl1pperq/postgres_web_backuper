import psycopg2
from config import *
from models import *


def get_schemas():
    result = []
    try:
        conn = psycopg2.connect(dbname="", host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database")
        databases = cursor.fetchall()
        cursor.close()
        conn.close()

    except Exception as error:
        print("Ошибка при работе с базой данных:", error)
        return []

    print("TESTORIA", f"DATABASES: {databases}")
    for database in databases:
        try:
            print("TESTORIA", f"WILL CONNECT to {database[0]}")
            conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
                                    database=database[0])

            cursor = conn.cursor()
            cursor.execute("SELECT schema_name FROM information_schema.schemata")

            schemas = cursor.fetchall()

            for schema in schemas:
                result.append((database[0], schema[0]))

            cursor.close()
            conn.close()
        except Exception as error:
            print("Ошибка при работе с базой данных:", error)

    return result


def create_records(targets):
    for database, schema in targets:
        record = Schema.query.filter_by(database=database, schema=schema).first()
        if not record:
            db.session.add(Schema(database=database, schema=schema, freq="never"))
    db.session.commit()

    return Schema.query.all()


def get_groups(records):
    groups = {}
    for record in records:
        if record.database not in groups:
            groups[record.database] = []
        groups[record.database].append(record)

    return groups
