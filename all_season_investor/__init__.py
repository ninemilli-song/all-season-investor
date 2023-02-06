"""
Fix the raise Exception When start:
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?

Add some code as below
 |
\/
"""
import pymysql
pymysql.install_as_MySQLdb()