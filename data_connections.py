import os
from lxml import etree
from MySQLdb import connect as connectMySQL
from pyodbc import connect as connectMSSQL
import logging

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

def dbLoadConfig(id):
    global SCRIPT_PATH

    with open(SCRIPT_PATH+"/connections.xml","r") as dbConfig:
        xml = dbConfig.read()
    dbConfig.close()
    parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
    config = etree.fromstring(xml, parser=parser)

    output = []
    
    itemGroup = config.iter("connection")
    for item in itemGroup:
        if id == None or item.get("id") == id:
            output.append({
                "title" : item.find('title').text,
                "mode" : item.find('mode').text,
                "host" : item.find('host').text,
                "port" : item.find('port').text,
                "db" : item.find('./structure/dbName').text,
                "uid" : item.find('./login/user').text,
                "pwd" : item.find('./login/pass').text,
                "gateway" : item.find('gateway').text
            })

    if not output:
        return None
            
    if id != None:
        return output[0]
            
    return output


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
                r'DRIVER={SQL Server};'
                r'SERVER='+host+';'
                r'DATABASE='+db+';'
                r'UID='+uid+';'
                r'PWD='+pwd+';'
            )
        elif mode == "mysql":
            conn = connectMySQL(host=host, user=uid, passwd=pwd, db=db)

    return conn


def fixQuery(mode,query):
    #Adjust query to fit selected database model

    return query

