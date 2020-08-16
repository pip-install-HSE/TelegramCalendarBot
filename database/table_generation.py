tables = {}

tables["users"] = {
    "id": "SERIAL PRIMARY KEY",
    "tg_id": "BIGINT",
    "name": "VARCHAR(16)",
    "phone": "VARCHAR(16)",
    "day": "SMALLINT",
    "month": "SMALLINT",
    "year": "SMALLINT",
}
# docker exec -it my-postgres bash

from database.base import Database


def generate():
    db = Database("jdbc:postgresql://185.255.132.17:5432;user=postgres;password=example;")
    for table in tables.keys():
        columns = ["%s %s" % (column, type) for column, type in list(tables[table].items())]
        query = "CREATE TABLE IF NOT EXISTS {table} ({columns})".format(table=table,
                                                                    columns=", ".join(columns))  # IF NOT EXISTS
        print(query)
        db.query(query)
    db.commit()
    db.close()
