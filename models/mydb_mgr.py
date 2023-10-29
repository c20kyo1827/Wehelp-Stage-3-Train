from mysql.connector import connect
from mysql.connector import Error
from mysql.connector import pooling
import argparse
import logging
import sys
import os


logging.root.name = "RDS db manager"
logging.basicConfig(level=logging.INFO,
                format='[%(levelname)-7s] %(name)s - %(message)s',
                stream=sys.stdout)
class mydb_mgr:
    def __init__(self):
        self._mypool = None

    def reset(self):
        self.connect()
        self.reset_database()
        self.reset_table()

    def init(self):
        self.connect()

    def connect(self):
        self._mypool = pooling.MySQLConnectionPool(
            pool_name="my_py_pool",
            pool_size=3,
            pool_reset_session=True,
            host=os.getenv("RDS_HOST"),
            port=os.getenv("RDS_PORT"),
            user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_ROOT_PASSWD")
        )
        logging.info("Connection Pool Name - {}".format(self._mypool.pool_name))
        logging.info("Connection Pool Size - {}".format(self._mypool.pool_size))

    def connect_and_run(self, func, is_commit=False):
        if self._mypool==None:
            return
        result = None
        try:
            mydb = self._mypool.get_connection()
            if mydb.is_connected():
                mycursor = mydb.cursor()
                result = func(mycursor)

                if is_commit:
                    mydb.commit()

        except Error as e:
            mydb.rollback()
            logging.error("Error while connecting to MySQL using Connection pool : {}".format(e))
            logging.info("Rollback...")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
            return result

    def reset_database(self):
        def run(cursor):
            cursor.execute("DROP DATABASE IF EXISTS mydb")
            cursor.execute("CREATE DATABASE mydb")
        self.connect_and_run(run)

    def reset_table(self):
        def run(cursor):
            cursor.execute("USE mydb")
            cursor.execute("DROP TABLE IF EXISTS message")
            # Attractions
            cursor.execute( \
                "CREATE TABLE message( \
                    id bigint AUTO_INCREMENT, \
                    content varchar(255) NOT NULL, \
                    new_image varchar(255) NOT NULL, \
                    PRIMARY KEY(id) \
                )" \
            )
        self.connect_and_run(run)

    # Test & Debug
    def runSQLCmd(self, cmd):
        def run(cursor):
            cursor.execute("USE mydb")
            logging.info("Run the command in mysql : " + cmd)
            cursor.execute(cmd)
            logging.info(str(cursor.fetchall()))
        self.connect_and_run(run, True)

    def show(self):
        def run(cursor):
            cursor.execute("USE mydb")
            table = ["message"]
            for t in table:
                cmd = "SELECT * FROM " + t
                cursor.execute(cmd)
                member_info = cursor.fetchall()
                for x in member_info: logging.info(x)
        self.connect_and_run(run)

    def add_message(self, content, img_url):
        def add_attraction(cursor):
            sql = "INSERT INTO message  \
                    (content, new_image) VALUES (%s, %s)"
            val = (content, img_url)
            cursor.execute("USE mydb")
            cursor.execute(sql, val)
        self.connect_and_run(add_attraction, True)


    # Get function
    def get_all_message(self):
        def run(cursor):
            cursor.execute("USE mydb")
            sql = "SELECT * FROM message ORDER BY id DESC"
            cursor.execute(sql, )
            return cursor.fetchall()
        return self.connect_and_run(run)

# The argument parser
def Argument():
    parser = argparse.ArgumentParser(description="Mysql db manager")
    list_of_mode = ["reset"]
    parser.add_argument('-m', '--mode', type=str, choices=list_of_mode, default="init", help="specify the mode, current support = {}, default = init".format(list_of_mode))
    parser.add_argument('-s', '--show', default=False, action="store_true", help="show the current database")
    parser.add_argument('-c', '--command', type=str, help="run testing command in mydb")
    return parser.parse_args()

if __name__=="__main__":
    flow = mydb_mgr()
    arg = Argument()

    if arg.mode=="reset":
        flow.reset()
    else:
        flow.init()

    if arg.show:
        flow.show()

    if arg.command != None:
        flow.runSQLCmd(arg.command)