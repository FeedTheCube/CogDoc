from src.Query.DataItem.DataItem import DataItem as DataItem
from src.Query.DetailFilter.DetailFilter import DetailFilter as DF

class Query(object):
    """description of class"""
    def __init__(self, _name, _source, _joins, _dataItems, _filters, _slicers, _element):
        self.name = _name
        self.source = _source
        self.joins = _joins
        self.dataItems = _dataItems
        self.filters = _filters
        self.slicers = _slicers
        self.element = _element

    def getQueries(xmlSpec, namespace):
        print("retreiving queries")
        queries=[]
        queriesIter = xmlSpec.iter(namespace + "query")
        for query in queriesIter:
            if query[0][0].tag == namespace+"queryRef":
                source = query[0][0].get("refQuery")
            if query[0][0].tag == namespace+"model":
                source = "model"
            qry = Query(
                    _name = query.get("name"),
                    _source = source,
                    _joins = None,
                    _dataItems = DataItem.getDataItems(query, namespace),
                    #getDataItems,
                    _filters = DF.getDetailFilters(query, namespace),
                    _slicers = None,
                    _element = query
                )
            queries.append(qry)
        return queries
      
    def printQueryStats(self):
          print(
                "QueryName: ", self.name, 
                ", Source: ", self.source,
                ", DataItems: ", len( self.dataItems ),
                ", Filters: ", len(self.filters)
                )
