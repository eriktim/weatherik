import psycopg2

class Database(object):

  __host = "localhost"
  __port = 5432
  __database = "weatherik"
  __user = "weatherik_user"
  __password = "weatherik_password"

  __conn = None
  __cursor = None

  def __init__(self):
    self.__conn = psycopg2.connect(database=self.__database,
                            host=self.__host,
                            port=self.__port,
                            user=self.__user,
                            password=self.__password)
    self.__cursor = self.__conn.cursor()

  def __del__(self):
    self.__cursor.close()
    self.__conn.close()

  def insert(self, table, data):
    if not table or not data:
      return False

    holders = ["%s" for x in range(len(data))]

    query = "INSERT INTO " + table + " (" + ','.join(data.keys()) + ") VALUES (" + ','.join(holders) + ");"
    self.__cursor.execute(query, data.values())
    self.__conn.commit()

    return self.__cursor.rowcount >= 0
