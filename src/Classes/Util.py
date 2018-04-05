import os

from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query
from src.Classes.Report import Report
from lxml import etree

import dataConnections as DC


class Util(object):
    #Used for static methods/functions

    def loadInputFile(path, filename):
        if(path):
            with open(path,'r') as xmlFile:
                spec = xmlFile.read()
            xmlFile.close()
            parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
            xmlData = etree.fromstring(spec, parser=parser)
            ns = "{" + xmlData.nsmap[None] + "}"

            report = Util.getSingleReport(xmlData, ns, reportName=filename)
            return report


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

            new.queries = Util.getQueries(item, namespace, report=name)
            new.dataItems = Util.getDataItems(item, namespace)

            reports.append(new)

        return reports


    def getSingleReport(element, namespace, reportName = None, CMID=None):

        #IMPROVE - The below chunk of code seems less than ideal. I imagine there's a much better way to handle it.

        name=''
        useStyleVersion = element.get('useStyleVersion')
        expressionLocale = element.get('expressionLocale')
        viewPagesAsTabs = element.get('viewPagesAsTabs')
        if (reportName):
            name = reportName
        else:
            name = element.find(namespace+'reportName').text
            # for tag in nameTags:
             #   name = tag[0].text
        modelTag = element.find(namespace+'modelPath')
        if modelTag is not None:
            modelPath = modelTag.get('path')
        else:
            modelPath = 'not found'

        report = Report(CMID=CMID, name=name,xmlns=namespace, useStyleVersion=useStyleVersion, expressionLocale=expressionLocale, viewPagesAsTabs = viewPagesAsTabs, modelPath=modelPath, element=element)
        report.queries = Util.getQueries(element, namespace, report=name, modelPath=modelPath)
        report.dataItems = Util.getDataItems(element, namespace)

        return report

    def getQueries(element, namespace, report, modelPath):
        queries = []
        
        itemGroup = element.iter(namespace + "query")
        for item in itemGroup:
            #item = objectify.deannotate(item[0][0], cleanup_namespaces=True)
            startPos = item.tag.find(namespace)+len(namespace)
            sourceTag= item.find(namespace+'source')
            source = item[0][0].tag[startPos:]
            if source=='joinOperation':
                joins = True
                sourceName = ''
                queryRefs = item.iter(namespace+'queryRef')
                for tag in queryRefs:
                     sourceName += tag.get('refQuery')+', '
                sourceName = sourceName[:-2]
            elif (source == 'queryRef'):
                joins = False
                sourceIter = item.iter(namespace+source)
                for src in sourceIter:
                    sourceName = src.attrib['refQuery']
            elif (source=='metadataPath'):
                joins = False
                sourcePath = sourceTag.find(namespace+'metadataPath').get('path')
            elif (source=='model'):
                joins = False
                mdl = element.find('modelPath')

                sourceName = "not there yet."

            else:
                join = False
                sourceName = ''

            queries.append( 
                Query(
                    report = report,
                    name = item.get("name"),
                    source = source,
                    sourceName = sourceName,
                    joins = joins,
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
            exp = item.find(".//"+namespace+"expression")

            dataItems.append(
                DataItem(
                    name = item.get("name"),
                    aggregate = item.get("aggregate"),
                    rollupAggregate = item.get("rollupAggregate"),
                    sort = item.get("sort"),
                    expression = exp.text,
                    element = item
                )
            )
        
        return dataItems
    

    def getDetailFilters(element, namespace):
        detailFilters = []
        
        itemGroup = element.iter(namespace + "detailFilter")
        if itemGroup:
            for item in itemGroup:
                if item.get("use"):
                    use = item.get("use")
                else:
                    use = "required"

                postAutoAggregation = item.get("postAutoAggregation")

                detailFilters.append(

                    DetailFilter(
                        expression = item[0].text,
                        usage = use,
                        postAutoAggregation = postAutoAggregation,
                        element = item
                    )
                )
        
        return detailFilters


    def HTMLloadInputFile(xmlFile, filename):
        if(xmlFile):

            spec = xmlFile.read()
            xmlFile.close()

            parser = etree.XMLParser(recover=True, encoding="ISO-8859-1", remove_blank_text=True, ns_clean=True)
            xmlData = etree.fromstring(spec, parser=parser)

            ns = "{" + xmlData.nsmap[None] + "}"


            #TEMPORARY OUTPUT SETUP

            report = Util.getSingleReport(xmlData, ns, reportName=filename)
            
            return report
        return None

    def DBloadInputFile(strXML, reportName=None, CMID=None):
        if(strXML):
            parser = etree.XMLParser(remove_blank_text=True, ns_clean=True, recover=True)
            xmlData = etree.fromstring(strXML, parser=parser)
            ns = "{" + xmlData.nsmap[None] + "}"
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
        with open('src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()
        
        rows = Util.queryDB(connectionID = connectionID, query=query)
        return rows

    def getReportByID(connectionID, CMID):
        with open('src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()

        with open('src/Views/_SQL_Filter_andCMID.sql', 'r') as sqlFilter:
            query += sqlFilter.read()
        sqlFilter.close()

        query = query.format(CMID)
        rows = Util.queryDB(connectionID=connectionID, query=query)

        report = Util.DBloadInputFile(strXML=rows[0][2],reportName=rows[0].NAME, CMID = rows[0].CMID)
        return report