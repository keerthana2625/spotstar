import pymysql

pymysql.version_info = (2, 2, 8, 'final', 0)
pymysql.install_as_MySQLdb()

# Mock versions so Django's mysqlclient check passes
import sys
import MySQLdb
MySQLdb.__version__ = "2.2.8"
MySQLdb.version_info = (2, 2, 8, 'final', 0)
sys.modules['MySQLdb'] = MySQLdb
