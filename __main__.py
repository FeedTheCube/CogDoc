import os
import dataConnections as DC
import logging
from flask import Flask, request, url_for, redirect
from flask.templating import render_template
from src.Classes.Report import Report
from src.Classes.GUI import GUI
from src.Classes.Query import Query
from src.Classes.Util import Util
from werkzeug.utils import secure_filename
from lxml import etree as etree


UPLOAD_FOLDER = './UploadData'
ALLOWED_EXTENSIONS = set(['xml', 'txt'])
BLOCKSIZE = 1048576 # or some other, desired size in bytes


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def displayHome():
    return render_template('index.html', title="CogDoc Home")


@app.route('/reports', methods=["GET","POST"])
def listReports():
    reports = []
    rows = Util.getAllReports("hyndman_mssql")
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID)) for row in rows]
    if len(reports)>0:
        keys = reports[0].json().keys()
        lstJSON = []
        [lstJSON.append(report.json()) for report in reports]

        return render_template('reports.html', reports=reports, keys = keys, json = lstJSON, title='Report List')


@app.route('/queries', methods=["GET", "POST"])
def listQueries():
    joins = request.args.get('joins')
    print(joins)
    reports = []
    allQueries = []
    queries=[]
    rows = Util.getAllReports("hyndman_mssql")
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID)) for row in rows]
    if len(reports)>0:
        for report in reports:
            rowsQ = Util.getQueries(report.element, report.xmlns, report=report.name)
            for query in rowsQ:
                allQueries.append(query)
    else:
        pass

    if ( joins=='True' ):
        print("joins=True")
        for query in allQueries:
            print(query.name + ":", query.joins )
            if query.joins==True:
                query.json().insert("report", report.name)
                queries.append(query)
    else:
        queries=allQueries

    return render_template("queries.html", queries = queries)



@app.route('/report/<string:cmid>', methods=["GET","POST"])
def displayReport(cmid):
    CMID = int(cmid)
    report = Util.getReportByID("hyndman_mssql", CMID)
    json = report.json()
    queries = []
    [queries.append(query) for query in report.queries]
    dataItems = report.dataItems
    element = etree.tostring(report.element,pretty_print=True).decode()

    return render_template('report.html', element=element, report=report, json=json, queries=queries, title=report.name)

    
@app.route('/settings', methods=["GET","POST"])
def displaySettings():
    databases = DC.dbLoadConfig(None)

    if request.method == 'POST':
        #Pass databases list to a function
        #Add a new connection to the list
        #Display list of connections as usual
        pass
    return render_template('settings.html',databases=databases)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # reports.append(Util.HTMLloadInputFile(file))

            # with codecs.encode( file, 'utf-8', 'ignore') as sourceFile:
            #    with codecs.open(file.filename, "w", "utf-8") as targetFile:
            #        while True:
            #            contents = sourceFile.read(BLOCKSIZE)
            #            if not contents:
            #                break
            #            targetFile.write(contents)

            return redirect(url_for('listReports'))

    return render_template('load_report.html')


@app.route('/trial')
def displayTrial():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=8180)