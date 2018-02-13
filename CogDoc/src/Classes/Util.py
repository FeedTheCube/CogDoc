import os
from _codecs import encode
import codecs
from _codecs import utf_8_encode
from src.Classes.Report import Report
from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query
from lxml import etree 
import dataConnections as DC

class Util(object):
    #Used for static methods/functions

    def loadInputFile(path):
        if(path):
            with open(path,'r') as xmlFile:
                spec = xmlFile.read()
            xmlFile.close()
            parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
            xmlData = etree.fromstring(spec, parser=parser)
            ns = "{" + xmlData.nsmap[None] + "}"


            #TEMPORARY OUTPUT SETUP

            report = Util.getSingleReport(xmlData, ns)
            
            #Build the output
            content = ""
            
            #Attributes
            XMLattributes = ""
            for item in report.json():
                value = report.json()[item]
                print(value)
                badge = ""
                if isinstance(value, int):
                    badge = "<span class='badge'><a href='#{}'>{}</a></span>".format(item,value)
                    value = ""

                XMLattributes += "<li class='list-group-item'>{}  {}  {}</li>".format(item, value, badge)
            
            print(XMLattributes)
            if XMLattributes != "":
                content += "<h2>Summary</h2><ul class='list-group'>{}</ul>".format(XMLattributes)

            #Queries
            lstQueries = Util.getQueries(xmlData, ns)
            lstQueriesJSON = [query.json() for query in lstQueries]
            content += Util.HTMLify(lstQueriesJSON, "queries")
            
            #Query Objects
            for query in lstQueries:
                #dataItems
                dataItems = Util.getDataItems(query.element, ns)
                dataItemsJSON = [item.json() for item in dataItems]
                content += Util.HTMLify(dataItemsJSON, "{}:  Data Items".format(query.name))
                #detailFilters
                detailFilters = Util.getDetailFilters(query.element, ns)
                detailFiltersJSON = [filter.json() for filter in detailFilters]
                content += Util.HTMLify(detailFiltersJSON, "{}: Filters".format(query.name)) 

         
            #Pages
            
            #Containers
            return content, report
        return None


    def getReports(element, namespace):
        reports = []

        itemGroup = element.iter(namespace + "report")
        for item in itemGroup:

            #IMPROVE - The below chunk of code seems less than ideal. I imagine there's a much better way to handle it.

            if item.attrib['useStyleVersion']:
                useStyleVersion = item.attrib['useStyleVersion']
            if item.attrib['expressionLocale']:
                expressionLocale = item.attrib['expressionLocale']
            if item.attrib['viewPagesAsTabs']:
                viewPagesAsTabs = item.attrib['viewPagesAsTabs']
            if item[5].text:
                name = item[5].text

            new = Report(name, namespace, useStyleVersion, expressionLocale, viewPagesAsTabs, item)

            new.queries = Util.getQueries(item, namespace)
            new.dataItems = Util.getDataItems(item, namespace)

            reports.append(new)

        return reports


    def getSingleReport(element, namespace, reportName = None, CMID=None):

        #IMPROVE - The below chunk of code seems less than ideal. I imagine there's a much better way to handle it.


        useStyleVersion = element.get('useStyleVersion')
        expressionLocale = element.get('expressionLocale')
        viewPagesAsTabs = element.get('viewPagesAsTabs')
        if (reportName):
            name = reportName
        else:
            name = element.find('reportName')[0].text

        report = Report(CMID=CMID, name=name,xmlns=namespace, useStyleVersion=useStyleVersion, expressionLocale=expressionLocale, viewPagesAsTabs = viewPagesAsTabs, element=element)

        report.queries = Util.getQueries(element, namespace)
        report.dataItems = Util.getDataItems(element, namespace)

        return report

    def getQueries(element, namespace):
        queries = []
        
        itemGroup = element.iter(namespace + "query")
        for item in itemGroup:
            if item[0][0].tag == namespace+"queryRef":
                source = item[0][0].get("refQuery")
            if item[0][0].tag == namespace+"model":
                source = "model"

            queries.append( 
                Query(
                    name = item.get("name"),
                    source = source,
                    joins = None,
                    dataItems = Util.getDataItems(item, namespace),
                    filters = Util.getDetailFilters(item, namespace),
                    slicers = None,
                    element = item
                )
            )
        
        return queries
        

    def getDataItems(element, namespace):
        dataItems = []
        
        itemGroup = element.iter(namespace+"dataItem")
        for item in itemGroup:
            dataItems.append(
                DataItem(
                    name = item.get("name"),
                    aggregate = item.get("aggregate"),
                    rollupAggregate = item.get("rollupAggregate"),
                    sort = item.get("sort"),
                    expression = item.find(".//expression"),
                    element = item
                )
            )
        
        return dataItems
    

    def getDetailFilters(element, namespace):
        detailFilters = []
        
        itemGroup = element.iter(namespace + "detailFilter")
        if itemGroup:
            for item in itemGroup:
                if item.get("usage"):
                    usage = item.get("usage")
                else:
                    usage = "required"
                
                detailFilters.append(
                    DetailFilter(
                        expression = item[0].text,
                        usage = usage,
                        element = item
                    )
                )
        
        return detailFilters


    def exportHTML(filename, title, header, content, footer):
        with open(os.getcwd()+"\\src\\templates\\template.html","r") as templateFile:
            template = templateFile.read()
        templateFile.close()

        template = template.replace("[[TITLE]]",title)
        template = template.replace("[[HEADER]]",header)
        template = template.replace("[[CONTENT]]",content)
        template = template.replace("[[FOOTER]]",footer)

        with open(filename,"w") as outFile:
            outFile.write(template)
        outFile.close()

    
    def HTMLify(listJSONs, title=None):
        #length of listJSONs
        if (len(listJSONs)>0):
            tableWidth = len(listJSONs[0].keys())
        else:
            return "<table class='table'><tr class='info'>{}: No Filters</table>".format(title)
        #skip empty jsons
        if (len(listJSONs)<1):
            pass
        
        #build the table
        html = "<table class='table table-striped'>"
        
        #set Headers
        if (title):
            html += "<thead id={1} class='thead-dark'><tr><th scope='col' colspan='{0}'>{1}</th></tr></thead>".format(tableWidth, title)
            
        headerLabelsHTML = ""
        for header in listJSONs[0].keys():
            headerLabelsHTML+="<th scope='col'>{}</th>".format(header)
        
        print(headerLabelsHTML)
        html += "<thead  class='thead-light'><tr>{}</tr></thead><tbody>".format(headerLabelsHTML)
        
        #set Records
        for item in listJSONs:
            rowValuesHTML = ""
            for field in item:
                rowValuesHTML+="<td scope='row' class='filterable-cell'>{}</td>".format(item[field])
            html += "<tr>{}</tr>".format(rowValuesHTML)
        
        #close the table
        html += "</tbody></table>"
        return html

    def HTMLloadInputFile(xmlFile):
        if(xmlFile):
            print(type(xmlFile))
            spec = xmlFile.read()
            xmlFile.close()

            parser = etree.XMLParser(recover=True, encoding="ISO-8859-1", remove_blank_text=True, ns_clean=True)
            xmlData = etree.fromstring(spec, parser=parser)

            ns = "{" + xmlData.nsmap[None] + "}"


            #TEMPORARY OUTPUT SETUP

            report = Util.getSingleReport(xmlData, ns)
            
            return report
        return None

    def DBloadInputFile(strXML, reportName=None, CMID=None):
        if(strXML):
            parser = etree.XMLParser(recover=True,  remove_blank_text=True, ns_clean=True)
            xmlData = etree.fromstring(strXML, parser=parser)

            ns = "{" + xmlData.nsmap[None] + "}"

            # TEMPORARY OUTPUT SETUP

            report = Util.getSingleReport(xmlData, ns, reportName, CMID=CMID)

            return report

        return None

    def queryDB(connectionID, query):
        config = DC.dbLoadConfig(connectionID)    #CHANGE - should be loaded once, not before every method call

        conn = DC.dbConnect(config)
        cursor = conn.cursor()

        query = DC.fixQuery(config['mode'],query)

        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows

    def getAllReports(connectionID):
        with open('../CogDoc/src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()
        
        rows = Util.queryDB(connectionID = connectionID, query=query)
        return rows

    def getReportByID(connectionID, CMID):
        with open('../src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()

        with open('../CogDoc/src/Views/_SQL_Filter_andCMID.sql', 'r') as sqlFilter:
            query += sqlFilter.read()
        sqlFilter.close()

        query = query.format(CMID)
        rows = Util.queryDB(connectionID=connectionID, query=query)
        print(rows[0].NAME)
        report = Util.DBloadInputFile(strXML=rows[0][2],reportName=rows[0].NAME, CMID = rows[0].CMID)
        return report