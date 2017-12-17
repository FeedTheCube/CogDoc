class DatItem(object):
    """description of class"""
    def __init__(self, _name, _aggregate, _rollupAggregate, _sort, _expression, _element):
        self.name = _name
        self.aggregate = _aggregate
        self.rollupAggregate = _rollupAggregate
        self.sort = _sort
        self.expression = _expression
        self.element = _element