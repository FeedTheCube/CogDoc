from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query
from src.Classes.Report import Report
from lxml import etree
import data_connections as DC


class Util(object):
    # Used for static methods/functions

    def getAllReports(connectionID):
        with open('src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()

        rows, gateway = Util.queryDB(connectionID=connectionID, query=query)
        return rows, gateway

    def getReportByID(connectionID, CMID):

        # Open the SQL files and assemble the SELECT statement
        with open('src/Views/_SQL_GetAllReports.sql', 'r') as sqlFile:
            query = sqlFile.read()
        sqlFile.close()
        with open('src/Views/_SQL_Filter_andCMID.sql', 'r') as sqlFilter:
            query += sqlFilter.read()
        sqlFilter.close()
        query = query.format(CMID)

        # retrieve the dataset and get the gateway link from the settings file and return the report object and gateway
        rows, gateway = Util.queryDB(connectionID=connectionID, query=query)
        report = Util.DBloadInputFile(strXML=rows[0][2], reportName=rows[0].NAME, CMID=rows[0].CMID, storeID=rows[0].STOREID)
        return report, gateway

    def getSingleReport(element, namespace, reportName = None, storeID=None, CMID=None):

        # IMPROVE - The below chunk of code seems less than ideal. I imagine there's a much better way to handle it.

        useStyleVersion = element.get('useStyleVersion')
        expressionLocale = element.get('expressionLocale')
        viewPagesAsTabs = element.get('viewPagesAsTabs')
        modelPath = element.find(namespace+'modelPath')
        name = reportName if reportName else element.find(namespace+'reportName').text


        report = Report(CMID=CMID,
                        storeID=storeID,
                        name=name,xmlns=namespace,
                        useStyleVersion=useStyleVersion,
                        expressionLocale=expressionLocale,
                        viewPagesAsTabs = viewPagesAsTabs,
                        modelPath=modelPath,
                        element=element)
        report.queries = Util.getQueries(element,
                                         namespace,
                                         report=name,
                                         modelPath=modelPath)
        report.dataItems = Util.getDataItems(element, namespace)

        return report

    def getQueries(element, namespace, report, modelPath):
        queries = []
        itemGroup = element.iter(namespace + "query")
        for item in itemGroup:
            #item = objectify.deannotate(item[0][0], cleanup_namespaces=True)
            sourceTag= item.find(namespace+'source')
            source = None
            sourceName = None
            joins = None
            if sourceTag != None:
                 source, sourceName, joins = Util.parse_source(query=item, sourceTag=sourceTag, namespace=namespace, modelPath=modelPath)

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

    def DBloadInputFile(strXML, reportName=None, CMID=None, storeID=None):
        if(strXML):
            parser = etree.XMLParser(remove_blank_text=True, ns_clean=True, recover=True)
            xmlData = etree.fromstring(strXML, parser=parser)
            ns = "{" + xmlData.nsmap[None] + "}"
            report = Util.getSingleReport(xmlData, ns, reportName, CMID=CMID, storeID=storeID)
            return report

        return None

    def queryDB(connectionID, query):
        config = DC.dbLoadConfig(connectionID)    #CHANGE - should be loaded once, not before every method call

        conn = DC.dbConnect(config)
        cursor = conn.cursor()

        query = DC.fixQuery(config['mode'],query)
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        return rows, config['gateway']

    def parse_source(query, sourceTag, namespace, modelPath):
        startPos =  len(namespace)
        source = sourceTag[0].tag[startPos:]

        if source == 'joinOperation':
            type = 'join'
            joins = True
            sourceName = ''
            queryRefs = query.iter(namespace + 'queryRef')
            for tag in queryRefs:
                sourceName += tag.get('refQuery') + ', '
            sourceName = sourceName[:-2]
        elif (source == 'queryRef'):
            joins = False
            sourceName = query.find(namespace + 'source')[0].get('refQuery')
        elif (source == 'metadataPath'):
            joins = False
            sourcePath = sourceTag.find(namespace + 'metadataPath').get('path')
            if sourcePath.find('package'):
                type = 'package'
                sourceName = Util.cognosNameFromPath(sourcePath, type)
            elif sourcePath.find('module'):
                type = 'module'
                sourceName = Util.cognosNameFromPath(sourcePath, type)
            else:
                type='unknown'
                sourceName='unknown'
            source = 'metadataPath:'+ type
        elif (source == 'model'):
            joins = False
            mdl = modelPath.text
            type = modelPath.get('type')
            if type==None:
                type='package'
            sourceName = Util.cognosNameFromPath(mdl, type)
            source = type
        else:
            joins = 'Unknown'
            sourceName = 'Unknown'

        return source, sourceName, joins

    def cognosNameFromPath(path, objectName):
        opener = "{0}[@name='".format(objectName)
        closer = "']"
        startPos = path.find(opener) + len(opener)
        cutPos = path[startPos:].find(closer) + startPos
        name = path[startPos:cutPos]
        return name