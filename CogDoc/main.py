
from lxml import etree
import xml.etree.ElementTree as ET
import src
from src.Query.Query import Query as Query


with open("DCL0001 - Position Detail Report.xml",'r') as xmlFile:
    spec = xmlFile.read()
xmlFile.close()
parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
xmlData = etree.fromstring(spec, parser=parser)
ns = "{" + xmlData.nsmap[None] + "}"

Query.getQueries(xmlData, ns)
