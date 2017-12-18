import os
from src.Classes.Util import Util as Util
from src.Classes.Query import Query as Query
from lxml import etree 


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(__location__+"\DCL0001 - Position Detail Report.xml",'r') as xmlFile:
    spec = xmlFile.read()
xmlFile.close()
parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
xmlData = etree.fromstring(spec, parser=parser)
ns = "{" + xmlData.nsmap[None] + "}"

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


