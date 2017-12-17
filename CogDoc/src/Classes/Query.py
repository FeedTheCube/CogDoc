from src.Classes.DatItem import DatItem
from src.Classes.DetFilter import DetFilter

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
    
    # By putting this method in the class, it implies that the class is a requirement for the method.
    # It also means as a developer, you have to remember the heirarchy of the dataset you're parsing.  
    # In this case, that doesn't make sense as an approach because we can capture all of any type of 
    #  element with a .iter("nameOfType")
    @classmethod
    def getQueries(cls, xmlSpec, namespace):
        print("retreiving queries")
        queries = []
        queriesIter = xmlSpec.iter(namespace + "query")
        for query in queriesIter:
            if query[0][0].tag == namespace+"queryRef":
                source = query[0][0].get("refQuery")
            if query[0][0].tag == namespace+"model":
                source = "model"
            q = Query(
                _name = query.get("name"),
                _source = source,
                _joins = None,
                _dataItems = DatItem.getDataItems(query, namespace),
                _filters = DetFilter.getDetailFilters(query, namespace),
                _slicers = None,
                _element = query
                )
            queries.append(q)
        return queries
    
    
    def JSON(self):
        return { 
            'name': self.name,
            'source': self.source,
            'joins': self.joins,
            'dataItems': len(self.dataItems),
            'filters': len(self.filters),
            'slicers': self.slicers
            }
