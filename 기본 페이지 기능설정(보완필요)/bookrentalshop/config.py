import cx_Oracle
DB_CONFIG = {
    'user': 'bookrentalshop',
    'password': '12345',
    'dsn': cx_Oracle.makedsn('localhost', 1521, service_name='XE' )
}



#학교 디비
# DB_CONFIG = {
#     'user': 'bookrentalshop',
#     'password': '12345',
#     'dsn': cx_Oracle.makedsn('210.119.14.73', 1521, service_name='XE' )
# }