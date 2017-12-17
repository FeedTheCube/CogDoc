import os
import src
import xml.etree.ElementTree as etree
from lxml import etree
from src.Classes.Util import Util
from src.Query.Query import Query as Query


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(__location__+"\DCL0001 - Position Detail Report.xml",'r') as xmlFile:
    spec = xmlFile.read()
xmlFile.close()
parser = etree.XMLParser(recover=True, remove_blank_text=True, ns_clean=True)
xmlData = etree.fromstring(spec, parser=parser)
ns = "{" + xmlData.nsmap[None] + "}"

queries = Util.getQueries(xmlData, ns)
for query in queries:
    query.printStats()
