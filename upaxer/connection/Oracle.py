import json
import os
import cx_Oracle
from upaxer.utils.Secret import get_secret
#from bson import json_util

oracle_Types = {
    'cursor': cx_Oracle.CURSOR,
    'numeric': cx_Oracle.NUMBER,
    'string': cx_Oracle.STRING
}


class Oracle:
    validar_lib = True
    def __init__(self):
        ambiente_local = True
        if ambiente_local:
            self.server = "bdupaxerdev.cvwnpg9hzinn.us-east-1.rds.amazonaws.com"
            self.port = 1521
            self.service_name = "UPAXDEV"
            self.user = "TSTUPAXER"
            self.password = "UpaXER2022@"
        else:
            self.db_info = get_secret(os.environ['SECRET_ORACLE'])
            self.server = self.db_info['server']
            self.port = self.db_info['port']
            self.service = self.db_info['service']
            self.user = self.db_info['user']
            self.password = self.db_info['password']
        connection = self.user + "/" + self.password + "@" + self.server + ":" + str(self.port) + "/" + self.service_name
            #self.conn = cx_Oracle.connect(connection)
            #self.cursor = self.conn.cursor()
        if ambiente_local:
            if Oracle.validar_lib:
                cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_8")
                Oracle.validar_lib = False

        self.conn = cx_Oracle.connect(connection)
        self.cursor = self.conn.cursor()
    def execute(self ,type, name, parameters=None):

            try:
                db_execute = self.cursor.callfunc(name, oracle_Types[type], keywordParameters=parameters) if parameters != None else self.cursor.callfunc(name, oracle_Types[type])
                if type == 'cursor':
                    columns = [field[0] for field in db_execute.description]
                    rows = db_execute.fetchall()
                    data = [dict(zip(columns, row)) for row in rows]
                    for d in data:
                        for key, value in d.items():
                            if isinstance(d[key], cx_Oracle.LOB):
                                d[key] = json.loads(str(value))
                    db_dto = {
                        "hasError": False,
                        "data": json.dumps(data)
                        #"data": json.dumps(data, default=json_util.default)
                    }
                else:
                    db_dto = {
                        "hasError": False,
                        "data": db_execute
                    }
            except Exception as e:
                db_dto = {
                    "hasError": True,
                    "data": str(e)
                }
            self.conn.close()
            return db_dto
