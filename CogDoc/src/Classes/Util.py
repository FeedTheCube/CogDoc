import os
from src.Classes.Report import Report
from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query
from lxml import etree 


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

            totalDataItems = 0
            totalFilters = 0

            reports = Util.getReports(xmlData, ns)

            for report in reports:
                print(report.json())

                for query in report.queries:
                    totalDataItems += len(query.dataItems)
                    totalFilters += len(query.filters)

                totalQueries = len(report.queries)
                print(
                    "DataItems: ", totalDataItems, 
                    "Filters: ", totalFilters,
                    "Queries: ", totalQueries
                    )
                [print(item.json()) for item in report.queries]

            return reports
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

            new = Report(namespace, useStyleVersion, expressionLocale, viewPagesAsTabs)

            new.queries = Util.getQueries(item, namespace)

            reports.append(new)

        return reports


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
                    expression = item[0].text,
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
        with open(os.getcwd()+"\\src\\Templates\\template.html","r") as templateFile:
            template = templateFile.read()
        templateFile.close()

        template = template.replace("[[TITLE]]",title)
        template = template.replace("[[HEADER]]",header)
        template = template.replace("[[CONTENT]]",content)
        template = template.replace("[[FOOTER]]",footer)

        with open(filename,"w") as outFile:
            outFile.write(template)
        outFile.close()