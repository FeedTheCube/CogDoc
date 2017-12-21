import os
from src.Classes.Report import Report
from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter
from src.Classes.Query import Query
from src.Classes.Style import Style


class Util(object):
    #Used for static methods/functions

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


    def getStyles(element, namespace):
        styles = []
        
        itemOuter = element.iter(namespace + "style")
        if itemOuter:
            for outer in itemOuter:

                print("Checking ",outer.tag)

                itemGroup = outer.iter(namespace + "*")
                if itemGroup:
                    previous = None

                    for item in itemGroup:

                        print("...Checking ",item.tag)

                        if item.tag == namespace + "defaultStyle" or item.tag == namespace + "CSS":
                            if item.get("refStyle"):
                                reference = item.get("refStyle")
                            else:
                                reference = ""

                            if item.get("value"):
                                css = item.get("value")
                            else:
                                css = ""
                
                            styles.append(
                                Style(
                                    parent = previous,
                                    reference = reference,
                                    css = css
                                )
                            )

                            previous = item     #CHECK - Is this always valid as a "parent" to the next style?
        
        return styles

    def exportHTML(filename, title, header, content, footer):
        with open(os.getcwd()+"\\src\\Templates\\template.html","r") as templateFile:
            template = templateFile.read()
        templateFile.close()

        template = template.replace("[[TITLE]]",title)
        template = template.replace("[[HEADER]]",header)
        template = template.replace("[[CONTENT]]",content)
        template = template.replace("[[FOOTER]]",footer)

        with open(os.getcwd()+"\\Output\\"+filename,"w") as outFile:
            outFile.write(template)
        outFile.close()


