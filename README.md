![Python](https://github.com/bclipp/easy_database/workflows/Python/badge.svg)

## easy_database

### description
This is a personal package used to hold code patterns used for relational ETL database access.

### Usage

environment setup
```
pyenv install 3.8.0
pyenv virtualenv 3.8.0 app_3.8
pyenv activate app_3.8

# for integration tests
export POSTGRES_PASSWORD=testing1234
export POSTGRES_USER=testing1234
export POSTGRES_DB=testing1234
export TABLE=customers
export INTEGRATION_TEST=True
```

python usagepyth    
```
database_manager = database_factory("postgresql")
database_manager.set_connection_string("...")
database_manager.open_conn()
database_manager.send_sql("SELECT * FROM TEST;")
database_manager.close_conn()
```