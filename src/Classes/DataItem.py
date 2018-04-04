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
        return {
            'Name':self.name,
            'Aggregate': self.aggregate,
            'Rollup Aggregate': self.rollupAggregate,
            'Sort': self.sort,
            'Expression': self.expression
            }