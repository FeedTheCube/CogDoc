from pyodbc import connect

conn = connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'
    r'SERVER=localhost\FTCSQL14;'
    r'DATABASE=cognos_cs;'
    r'UID=sa;'
    r'PWD=PASSWORD'
    )

def getAllReports():
    cursor = conn.cursor()
    with open('../CogDoc/src/Views/_SQL_GetAllReports', 'r') as sqlFile:
        query = sqlFile.read()

    sqlFile.close()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

