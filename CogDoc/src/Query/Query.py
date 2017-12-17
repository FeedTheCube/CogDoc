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

    def printStats(self):
        print(
            "QueryName: ", self.name, 
            ", Source: ", self.source,
            ", DataItems: ", len( self.dataItems ),
            ", Filters: ", len(self.filters)
            )
