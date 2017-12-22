import os
from src.Classes.Util import Util as Util
from src.Classes.Query import Query as Query
from lxml import etree 
from json import dumps, load
import json



#Get the files in the Input directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
listing  = os.listdir(__location__+"\\Input\\")

#Iterate the files, and export HTML for Report and Queries
for infile in listing:
    with open(__location__+"\\Input\\"+infile, 'r') as xmlFile:
        spec = xmlFile.read()
    xmlFile.close()
    parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
    xmlData = etree.fromstring(spec, parser=parser)
    ns = "{" + xmlData.nsmap[None] + "}"

    report = Util.getReports(xmlData, ns)
    
    #Build the output
    lstQueries = Util.getQueries(xmlData, ns)
    print(len(lstQueries))
    lstQueriesJSON = [query.json() for query in lstQueries]
    content = Util.HTMLify(lstQueriesJSON)

    #lstDataItems = Util.getDataItems(xmlData, ns)
    #print(len(lstDataItems))
    #lstDataItemsJSON = [dataItem.json() for dataItem in lstDataItems]
    #content += Util.HTMLify(lstDataItemsJSON)

    
    Util.exportHTML( report.name + ".html", report.name, report.name, content , "FOOTER")


