![Python](https://github.com/bclipp/easy_database/workflows/Python/badge.svg)

## easy_database

### description
This is a personal package used to hold code patterns used for relational ETL database access.

### Usage
```
database_manager = database_factory("postgresql")
database_manager.set_connection_string("...")
database_manager.open_conn()
database_manager.send_sql("SELECT * FROM TEST;")
database_manager.close_conn()
```