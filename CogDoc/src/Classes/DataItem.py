class DataItem(object):
    """description of class"""
    def __init__(self, name, aggregate, rollupAggregate, sort, expression, element):
        self.name = name
        self.aggregate = aggregate
        self.rollupAggregate = rollupAggregate
        self.sort = sort
        self.expression = expression
        self.element = element

    def json(self):
        {
        "name": self.name,
        "aggregate": self.aggregate,
        "rollupAggregate": self.rollupAggregate,
        "sort": self.sort,
        "expression": self.expression,
        }