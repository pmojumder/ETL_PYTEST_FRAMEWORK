MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "sys"

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

MYSQL_JDBC_URL = (
    f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver"

SOURCE_TABLE = "customer_source"
TARGET_TABLE = "customer_target"