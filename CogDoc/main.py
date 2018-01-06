import os
import dataConnections as DC
from flask.templating import render_template
from src.Classes.Report import Report
from src.Classes.GUI import GUI
from src.Classes.Query import Query
from src.Classes.Util import Util
from flask import Flask, request, url_for, redirect
from werkzeug.utils import secure_filename



#gui = GUI()
#gui.draw()

UPLOAD_FOLDER = 'D:/UploadData'
ALLOWED_EXTENSIONS = set(['xml', 'txt'])
BLOCKSIZE = 1048576 # or some other, desired size in bytes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID)) for row in DC.getAllReports()]
    if len(reports)>0:
        keys = reports[0].json().keys()
        lstJSON = []
        [lstJSON.append(report.json()) for report in reports]

        return render_template('reports.html', reports=reports, keys = keys, json = lstJSON)


if __name__=='__main__':
    app.run(port=8180)

