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


UPLOAD_FOLDER = './UploadData'
ALLOWED_EXTENSIONS = set(['xml', 'txt'])
BLOCKSIZE = 1048576 # or some other, desired size in bytes


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

           
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
            #reports.append(Util.HTMLloadInputFile(file))

            #with codecs.encode( file, 'utf-8', 'ignore') as sourceFile:
            #    with codecs.open(file.filename, "w", "utf-8") as targetFile:
            #        while True:
            #            contents = sourceFile.read(BLOCKSIZE)
            #            if not contents:
            #                break
            #            targetFile.write(contents)

            return redirect(url_for('listReports'))

    return render_template('load_report.html')

    
@app.route('/reports', methods=["GET","POST"])
def listReports():
    reports = []
    rows = Util.getAllReports("laptop_mssql")
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID)) for row in rows]
    if len(reports)>0:
        keys = reports[0].json().keys()
        lstJSON = []
        [lstJSON.append(report.json()) for report in reports]

        return render_template('reports.html', reports=reports, keys = keys, json = lstJSON)

        
@app.route('/report/<string:cmid>', methods=["GET","POST"])
def displayReport(cmid):
    CMID = int(cmid)
    print("get report: ", CMID)
    report = Util.getReportByID("laptop_mssql", CMID)
    json = report.json()
    queries = []
    [queries.append(query) for query in report.queries]
    dataItems = report.dataItems

    return render_template('report.html', report=report, json=json, queries=queries)

    
@app.route('/settings', methods=["GET","POST"])
def displaySettings():
    databases = DC.dbLoadConfig(None)

    if request.method == 'POST':
        #Pass databases list to a function
        #Add a new connection to the list
        #Display list of connections as usual
        pass
    return render_template('settings.html',databases=databases)
    
    
@app.route('/', methods=["GET","POST"])
def displayHome():
    return render_template('home.html')
    
    

    
if __name__=='__main__':
    app.run(port=8180)

