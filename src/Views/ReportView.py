from src.Classes.Util import Util
from src.Classes.Report import Report
from src.Classes.Query import Query
from src.Classes.DataItem import DataItem
from src.Classes.DetailFilter import DetailFilter

class ReportView(object):
    """description of class"""
    def displayReport(Report:report):
            
            #Build the output
            content = ""
            
            #Attributes
            XMLattributes = ""
            for item in report.json():
                value = report.json()[item]
                print(value)
                badge = ""
                if isinstance(value, int):
                    badge = "<span class='badge'><a href='#{}'>{}</a></span>".format(item,value)
                    value = ""

                XMLattributes += "<li class='list-group-item'>{}  {}  {}</li>".format(item, value, badge)
            
            print(XMLattributes)
            if XMLattributes != "":
                content += "<h2>Summary</h2><ul class='list-group'>{}</ul>".format(XMLattributes)

            #Queries
            lstQueries = Util.getQueries(xmlData, ns)
            lstQueriesJSON = [query.json() for query in lstQueries]
            content += Util.HTMLify(lstQueriesJSON, "queries")
            
            #Query Objects
            for query in lstQueries:
                #dataItems
                dataItems = Util.getDataItems(query.element, ns)
                dataItemsJSON = [item.json() for item in dataItems]
                content += Util.HTMLify(dataItemsJSON, "{}:  Data Items".format(query.name))
                #detailFilters
                detailFilters = Util.getDetailFilters(query.element, ns)
                detailFiltersJSON = [filter.json() for filter in detailFilters]
                content += Util.HTMLify(detailFiltersJSON, "{}: Filters".format(query.name)) 

         
            #Pages
            
            #Containers
    

