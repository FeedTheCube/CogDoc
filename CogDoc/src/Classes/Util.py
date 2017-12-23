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
            #lstQueries = Util.getQueries(xmlData, ns)
            #print(len(lstQueries))
            #lstQueriesJSON = [query.json() for query in lstQueries]

            content = Util.HTMLify(report)


            #RECOMMENDATION - I think we should move this to an export method. It just makes more sense for work to be done when the user clicks that button rather than before. 
                #It's also strangely slow on my computer and delays selecting an output file.



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
            #new.dataItems = Util.getDataItems(item, namespace)

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
        #report.dataItems = Util.getDataItems(element, namespace)

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

    
    def HTMLify(report):

        #build the table
        html = "<table class='table table-striped'>"

        #set Headings
        headingLabelsHTML = ""
        reportValues = ""
        for heading in report.json().keys():
            headingLabelsHTML += "<th scope='col'>{}</th>".format(heading.title())
            reportValues += "<td>{}</td>".format(report.json()[heading])
        html += "<thead class='thead-dark'><tr>{}</tr></thead>\n".format(headingLabelsHTML)
        html += "<tbody>\n"
        html += "<tr class=\"clickable\" onclick=\"return toggleChildren('report-" + report.name + "');\">{}</tr>\n".format(reportValues)


        #CHANGE - set up a proper numeric ID for reports, and use that for toggleChildren() 
        #ALSO - use it as a prefix or something for cell_group values so that there's no risk of two reports having the same values


        html += "<tbody id=\"report-" + report.name + "\" style=\"display: none;\">\n\n"

        #set Queries
        for index, query in enumerate(report.queries):
            cell_group = "cell-group-" + str(index)
            
            jsonQuery = query.json()

            #sub-table for queries
           
            html += "<tr><td></td><td colspan=\"4\">"  #CHANGE - Need to set up colspan to span (heading count) - 1 columns
            
            
            columns = ""
            for column in jsonQuery.keys():
                columns += "<td>" + str(jsonQuery[column]) + "</td>"
            html += "<tr class=\"clickable\" onclick=\"return toggleChildren('" + cell_group + "');\">{}</tr>".format(columns)

            html += "<tr><td></td><td colspan=\"4\">"  #CHANGE - Need to set up colspan to span (heading count) - 1 columns

            #sub-table for data items
            html += "<table class=\"cell-group\" id=\"" + cell_group + "\" style=\"display: none;\">\n"
            for dataItem in query.dataItems:
                html += "<tr>{}</tr>\n".format("<td colspan=\"4\">" + dataItem.name + "</td>")
            html += "</table>\n"

            html += "</td></tr>\n"

        html += "\n</tbody>\n" #end of report tbody

        #close the table
        html += "\n</tbody>\n</table>"

        return html