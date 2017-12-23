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

            report = Util.getSingleReport(xmlData, ns)

            #Build the output
            lstQueries = Util.getQueries(xmlData, ns)
            #print(len(lstQueries))
            lstQueriesJSON = [query.json() for query in lstQueries]
            content = Util.HTMLify(lstQueriesJSON)

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


    def getSingleReport(element, namespace):
        
        #IMPROVE - The below chunk of code seems less than ideal. I imagine there's a much better way to handle it.

        if element.attrib['useStyleVersion']:
            useStyleVersion = element.attrib['useStyleVersion']
        if element.attrib['expressionLocale']:
            expressionLocale = element.attrib['expressionLocale']
        if element.attrib['viewPagesAsTabs']:
            viewPagesAsTabs = element.attrib['viewPagesAsTabs']
        if element[5].text:
            name = element[5].text

        report = Report(name,namespace, useStyleVersion, expressionLocale, viewPagesAsTabs, element)

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

    
    def HTMLify(listJSONs):
        
        #skip empty jsons
        if (len(listJSONs)<1):
            pass
        
        #build the table
        html = "<table class='table table-striped'>"
  
        #set Headers
        headerLabelsHTML = ""
        for header in listJSONs[0].keys():
            headerLabelsHTML+="<th scope='col'>{}</th>".format(header)
        html += "<thead  class='thead-dark'><tr>{}</tr></thead><tbody>".format(headerLabelsHTML)
        
        #set Records
        for item in listJSONs:
            rowValuesHTML = ""
            for field in item:
                rowValuesHTML+="<td scope='row' class='filterable-cell'>{}</td>".format(item[field])
            html += "<tr>{}</tr>".format(rowValuesHTML)
        
        #close the table
        html += "</tbody></table>"
        return html