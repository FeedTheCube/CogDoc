import os
import json
from src.Classes.Report import Report
from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query


class Util(object):
    #Used for static methods/functions

    def getReports(element, namespace):
        if element.attrib['useStyleVersion']:
            useStyleVersion = element.attrib['useStyleVersion']
        if element.attrib['expressionLocale']:
            expressionLocale = element.attrib['expressionLocale']
        if element.attrib['viewPagesAsTabs']:
            viewPagesAsTabs = element.attrib['viewPagesAsTabs']
        if element[5].tag == (namespace+"reportName"):
            name = element[5].text
        new = Report(namespace, useStyleVersion, expressionLocale, viewPagesAsTabs, element, name)

        return new


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
       
        with open(os.getcwd()+"\\Output\\"+filename,"w+") as outFile:
            outFile.write(template)
        outFile.close()

    def HTMLify(listJSONs):
        if (len(listJSONs)<1):
            pass
        html = "<table class='table table-striped'>"
  
        #set Headers
        html += "<thead  class='thead-dark'><tr>"
        for header in listJSONs[0].keys():
            html+="<th scope='col'>" + header +"</th>"
        html += "</tr></thead>"
        
        #set Records
        for item in listJSONs:
            html += "<tr>"
            for field in item:
                html+="<td scope='row'>{}</td>".format(item[field])
            html += "</tr>"

        html += "</table>"
        return html