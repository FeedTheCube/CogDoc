print("By putting this static getXXX() methods in the class, it implies that the class is a requirement for the method.\n",
     "It also means as a developer, you have to remember the heirarchy of the dataset you're parsing.\n",
     "In this case, that doesn't make sense as an approach because we can capture all of any type of \n",
      "element with a .iter(\"nameOfType\).\n This branch has been abandoned"
      )

#import os
#from src.Classes.Query import Query 
#from src.Classes.DatItem import DatItem
#from src.Classes.DetFilter import DetFilter
#from lxml import etree


#__location__ = os.path.realpath(
#    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#with open(__location__+"\DCL0001 - Position Detail Report.xml",'r') as xmlFile:
#    spec = xmlFile.read()
#xmlFile.close()
#parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
#xmlData = etree.fromstring(spec, parser=parser)
#ns = "{" + xmlData.nsmap[None] + "}"

#print('---------QUERIES----------')
#queries = Query.getQueries(xmlData, ns)
#for query in queries:
#    print('---------QUERY----------')
#    print(query.JSON())
#    print()
#    print('---------DATA ITEMS----------')
#    for dataItem in query.dataItems:
#        print(dataItem.JSON())
#    filters = query.filters
#    if len(filters)>0:
#        print('---------FILTERS----------')
#        for filter in query.filters:
#            print(filter.JSON())
#    print()
