import data_connections as dc
from flask import Flask, request, redirect, flash, session
from flask_session import Session
from flask.templating import render_template
import werkzeug.utils
from lxml import etree as etree
from src.Classes.Util import Util
from werkzeug.contrib.fixers import LighttpdCGIRootFix


app = Flask( __name__ )
app.secret_key = 'yo mamma!'
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)

UPLOAD_FOLDER = './UploadData'
ALLOWED_EXTENSIONS = set(['xml', 'txt'])
BLOCKSIZE = 1048576 # or some other, desired size in bytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.template_filter('urlencode')
def urlencode_filter(s):
    print('before: ',s)
    for item in ['.','\'','\\', ' ']:
        s = s.replace(item,'')
    print('after: ',s)
    return s

@app.route('/', methods=["GET", "POST"])
def displayHome():
    return render_template('index.html', title="CogDoc Home")


@app.route('/reports', methods=["GET","POST"])
def listReports():
    reports = []
    rows, gateway = Util.getAllReports("hyndman_mssql")
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID, storeID=row.STOREID)) for row in rows]
    if len(reports)>0:
        keys = reports[0].json().keys()
        lstJSON = []
        [lstJSON.append(report.json()) for report in reports]

        return render_template('reports.html', reports=reports, keys = keys, json = lstJSON, title='Report List', gateway=gateway)


@app.route('/queries', methods=["GET", "POST"])
def listQueries():
    joins = request.args.get('joins')
    reports = []
    allQueries = []
    queries=[]
    rows, gateway = Util.getAllReports("hyndman_mssql")
    [reports.append(Util.DBloadInputFile(row[2], reportName=row.NAME, CMID=row.CMID)) for row in rows]
    if len(reports)>0:
        for report in reports:
            rowsQ = Util.getQueries(report.element, report.xmlns, report=report.name, modelPath=report.modelPath)
            for query in rowsQ:
                allQueries.append(query)
    else:
        pass

    if ( joins=='True' ):
        print("joins=True")
        for query in allQueries:
            print(query.name + ":", query.joins )
            if query.joins==True:
                queries.append(query)
    else:
        queries=allQueries

    return render_template("queries.html", title='Queries', queries = queries, gateway=gateway)



@app.route('/report/<string:cmid>', methods=["GET","POST"])
def displayReport(cmid):
    CMID = int(cmid)
    report, gateway = Util.getReportByID("hyndman_mssql", CMID)
    json = report.json()
    queries = []
    [queries.append(query) for query in report.queries]
    dataItems = report.dataItems
    element = etree.tostring(report.element,pretty_print=True).decode()

    return render_template('report.html', element=element, report=report, json=json, queries=queries, title=report.name, gateway=gateway)

    
@app.route('/settings', methods=["GET","POST"])
def displaySettings():
    databases = dc.dbLoadConfig(None)
    if request.method == 'POST':
        #Pass databases list to a function
        #Add a new connection to the list
        #Display list of connections as usual
        pass
    return render_template('settings.html',databases=databases, title='Settings')


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
            filename = werkzeug.utils.secure_filename(file.filename)
            print(filename)

            report=Util.HTMLloadInputFile(file, filename )
            element = etree.tostring(report.element, pretty_print=True).decode()
            # with codecs.encode( file, 'utf-8', 'ignore') as sourceFile:
            #    with codecs.open(file.filename, "w", "utf-8") as targetFile:
            #        while True:
            #            contents = sourceFile.read(BLOCKSIZE)
            #            if not contents:
            #                break
            #            targetFile.write(contents)

            return render_template('report.html', element=element, report=report, json=report.json, queries=report.queries, title=report.name)

    return render_template('load_report.html', title='Upload a Report')


@app.route('/trial', methods = ['GET', 'POST'])
def displayTrial():
    print('hello?')
    if request.method=='POST':
        print('hello')
        f = request.form
        print("f['userid']", f['userid'])
        session['user']= f['userid']
        print(session['user'])
        flash('Signed in...')
        return render_template('iFrameSample.html')


    return render_template('login.html', title='The Lab')

@app.route('/iFrameSample.html')
def displayiFrameSample():
    return render_template('iFrameSample.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html', title="404")

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
