import sqlalchemy


def init_connection_engine():
    db_config = {
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,

        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.

        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds

        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
    }
    return init_tcp_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    db_user = "sqlserver"
    db_pass = "sH8Z3wQnqmWYhfF"
    db_name = "IoT_db"
    db_private_host = "10.20.128.3:1433"
    #ssl_args = {'ssl_ca': 'ssl/server-ca.pem'}

    host_args = db_private_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    # SQL Server drivers don't account for this
    if db_hostname == "localhost":
        db_hostname = "127.0.0.1"

    pool = sqlalchemy.create_engine(

        # mssql+pytds://<db_user>:<db_pass>@/<host>:<port>/<db_name>?driver=ODBC+Driver+17+for+SQL+Server
        sqlalchemy.engine.url.URL.create(
            "mssql+pytds",
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_private_host,
        ),
        **db_config,
    )
    return pool


def create_connection():
    return init_connection_engine()
