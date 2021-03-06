class Query(object):
    """description of class"""
    def __init__(self, name, source, joins, dataItems, filters, slicers, element):
        self.name = name
        self.source = source
        self.joins = joins
        self.dataItems = dataItems
        self.filters = filters
        self.slicers = slicers
        self.element = element

    def json(self):
        return {
            'name': self.name,
            'source': self.source,
            'joins': self.joins,
            'dataItems': len( self.dataItems ),
            'filters': len(self.filters),
            'slicers': self.slicers,
            }