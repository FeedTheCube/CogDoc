class DetailFilter(object):
    """description of class"""
    def __init__(self, expression, usage, postAutoAggregation, element):
        self.expression = expression
        self.usage = usage
        self.postAutoAggregation = postAutoAggregation
        self.element = element

    def json(self):
        return {
            "Expression": self.expression,
            "Usage":self.usage,
            "After Auto Aggregation":self.postAutoAggregation
            }