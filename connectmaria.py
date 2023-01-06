
# this file is just to check
# the kali original system mariadb 
# connection settings.

# Module Import
import mariadb
import sys

# Instantiate Connection
try:
   conn = mariadb.connect(
      host="localhost",
      port=5009,
      user="user",
      password="user??")
   print("Connected!!!")
except mariadb.Error as e:
   print(f"Error connecting to the database: {e}")
   sys.exit(1)

conn.close()
