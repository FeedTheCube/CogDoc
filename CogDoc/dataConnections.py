from lxml import etree
from MySQLdb import connect as connectMySQL
from pyodbc import connect as connectMSSQL
import logging

def dbLoadConfig(id):
    with open("./connections.xml","r") as dbConfig:
        xml = dbConfig.read()
    dbConfig.close()
    parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
    config = etree.fromstring(xml, parser=parser)

    itemGroup = config.iter("connection")
    for item in itemGroup:
        if item.get("id") == id:
            return {
                "mode" : item.find('mode').text,
                "host" : item.find('host').text,
                "port" : item.find('port').text,
                "db" : item.find('./structure/dbName').text,
                "uid" : item.find('./login/user').text,
                "pwd" : item.find('./login/pass').text
            }

    return None


def dbConnect(config):
    conn = None

    if config != None:
        mode = config["mode"]
        host = config["host"]
        port = config["port"]
        db = config["db"]
        uid = config["uid"]
        pwd = config["pwd"]

        if mode == "mssql":
            conn = connectMSSQL(
                r'DRIVER={ODBC Driver 11 for SQL Server};'
                r'SERVER='+host+';'
                r'DATABASE='+db+';'
                r'UID='+uid+';'
                r'PWD='+pwd
            )
        elif mode == "mysql":
            conn = connectMySQL(host=host, user=uid, passwd=pwd, db=db)

    return conn


def fixQuery(mode,query):
    #Adjust query to fit selected database model

    return query


def getAllReports():
    config = dbLoadConfig("hyndman_mssql")    #CHANGE - should be loaded once, not before every method call

    conn = dbConnect(config)
    cursor = conn.cursor()
    with open('../CogDoc/src/Views/_SQL_GetAllReports', 'r') as sqlFile:
        query = sqlFile.read()

    sqlFile.close()

    query = fixQuery(config['mode'],query)

    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()

    return rows

